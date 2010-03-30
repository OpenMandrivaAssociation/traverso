%define name    traverso
%define version 0.49.1
%define release %mkrel 3
Name:           %{name}
Version:        %{version}
Release:        %{release}
Url:            http://traverso-daw.org/
License:        GPLv2+ and LGPL2+
Group:          Sound
Summary:        Cross Platform Multitrack Audio Recording and Editing Suite
Source:         http://traverso-daw.org/download/releases/current/%{name}-%{version}.tar.gz
Patch0:		traverso-0.49.1-fix-str-fmt.patch
BuildRequires:  cmake qt4-devel glib2-devel fftw-devel
BuildRequires:  libalsa-devel libjack-devel libportaudio-devel 
BuildRequires:  libsndfile-devel libsamplerate-devel redland-devel 
BuildRequires:  rasqal-devel raptor-devel desktop-file-utils
BuildRequires:  libflac-devel libvorbis-devel libwavpack-devel libmad-devel
BuildRequires:  slv2-devel >= 0.6.1

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Traverso is a free, cross platform multitrack audio recording and editing suite,
with an innovative and easy to master User Interface. It's suited for both
the professional and home user, who needs a robust and solid DAW.

%prep
%setup -q
%patch0 -p0

%build
%cmake_qt4 -DWANT_MP3_DECODE=ON \
           -DWANT_MP3_ENCODE=OFF \
           -DWANT_OPENGL=ON \
           -DWANT_PORTAUDIO=ON \
           -DUSE_SYSTEM_SLV2_LIBRARY=ON
%make

%install
rm -fr %buildroot
%makeinstall_std -C build

mkdir -p %buildroot%_datadir
cp -fr resources/freedesktop/icons %buildroot%_datadir/
install -D resources/traverso.desktop %buildroot%_datadir/applications/%name.desktop
install -D resources/x-traverso.xml %buildroot%_datadir/mime/packages/x-traverso.xml

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYRIGHT ChangeLog HISTORY README TODO
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/*.xml
%{_iconsdir}/*/*/*
