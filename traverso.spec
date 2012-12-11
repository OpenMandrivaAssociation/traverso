%global sse_cxxflags %{optflags}
%global sse_cmakeflags -DHOST_SUPPORTS_SSE:BOOL=FALSE
%ifarch %{ix86}
%global with_sse %{!?_without_sse:1}%{?_without_sse:0}
%if %{with_sse}
%global sse_cxxflags -DSSE_OPTIMIZATIONS -DARCH_X86 %{optflags}
%global sse_cmakeflags -DHOST_SUPPORTS_SSE:BOOL=TRUE -DIS_ARCH_X86:BOOL=TRUE
%endif
%endif
%ifarch ia64 x86_64
%global with_sse 1
%global sse_cxxflags -DSSE_OPTIMIZATIONS -DUSE_XMMINTRIN -DARCH_X86 -DUSE_X86_64_ASM %{optflags}
%global sse_cmakeflags -DHOST_SUPPORTS_SSE:BOOL=TRUE -DIS_ARCH_X86_64:BOOL=TRUE
%endif


Name:           traverso
Version:        0.49.2
Release:        %mkrel 5
Url:            http://traverso-daw.org/
License:        GPLv2+ and LGPLv2+
Group:          Sound
Summary:        Cross Platform Multitrack Audio Recording and Editing Suite
Source0:        http://traverso-daw.org/download/releases/current/%{name}-%{version}.tar.gz
Patch0:		traverso-0.49.1-fix-str-fmt.patch
BuildRequires:  cmake qt4-devel pkgconfig(glib-2.0) pkgconfig(fftw3)
BuildRequires:  alsa-oss-devel pkgconfig(jack) libportaudio-devel 
BuildRequires:  pkgconfig(sndfile) pkgconfig(samplerate) redland-devel 
BuildRequires:  rasqal-devel raptor-devel desktop-file-utils
BuildRequires:  pkgconfig(flac) pkgconfig(vorbis) libwavpack-devel libmad-devel
BuildRequires:  slv2-devel >= 0.6.1
BuildRequires:	pkgconfig(raptor2)
BuildRequires:	pkgconfig(slv2)
BuildRequires:	pkgconfig(lv2core)
Patch1:		traverso-0.49.2-desktop.patch
Patch2:		traverso-0.49.2-gold.patch
Patch3:		traverso-0.49.2-gcc47.patch	
Patch4:		traverso-0.49.1-slv2.patch
Patch5:		%{name}-linking.patch
Patch6:		traverso-link.patch

%description
Traverso is a free, cross platform multi-track audio recording and editing
suite, with an innovative and easy to master User Interface. It's suited for
both the professional and home user, who needs a robust and solid DAW.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1

# Fix permission issues
chmod 644 ChangeLog TODO
for ext in h cpp; do
   find . -name "*.$ext" -exec chmod 644 {} \;
done

# To match the freedesktop standards
sed -i -e '\|^MimeType=.*[^;]$|s|$|;|' \
    resources/%{name}.desktop

# We use the system slv2, so just to make sure
rm -fr src/3rdparty/slv2

# For proper slv2 detection
sed -i 's|libslv2|slv2|g' CMakeLists.txt



%build
%cmake_qt4 -DWANT_MP3_DECODE=ON \
           -DWANT_MP3_ENCODE=OFF \
           -DWANT_OPENGL=ON \
           -DWANT_PORTAUDIO=ON \
	   -DDETECT_HOST_CPU_FEATURES=OFF \
	   -DCXX_FLAGS:STRING="%{sse_cxxflags}" \
           %{sse_cmakeflags} \
           -DUSE_SYSTEM_SLV2_LIBRARY=ON
%make

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_iconsdir}/hicolor
cp -r resources/freedesktop/icons/*x* %{buildroot}%{_iconsdir}/hicolor/
install -D resources/traverso.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -D -m 644 resources/x-traverso.xml %{buildroot}%{_datadir}/mime/packages/x-traverso.xml

desktop-file-install --vendor="" \
		--remove-key="Encoding" \
		--remove-key="Path" \
		--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%name.desktop

%files
%doc AUTHORS COPYRIGHT ChangeLog HISTORY README TODO
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/*.xml
%{_iconsdir}/hicolor/*/*/*
