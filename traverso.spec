%define name    traverso
%define version 0.42.0
%define release %mkrel 1
Name:           %{name}
Version:        %{version}
Release:        %{release}
Url:            http://traverso-daw.org/
License:        GPLv2+ and LGPL2+
Group:          Sound
Summary:        Cross Platform Multitrack Audio Recording and Editing Suite
Source:         http://traverso-daw.org/download/releases/current/%{name}-%{version}.tar.gz
BuildRequires:  cmake qt4-devel glib2-devel fftw-devel
BuildRequires:  libalsa-devel libjack-devel libportaudio-devel 
BuildRequires:  libsndfile-devel libsamplerate-devel redland-devel 
BuildRequires:  rasqal-devel libraptor-devel desktop-file-utils
BuildRequires:  libflac-devel libvorbis-devel libwavpack-devel libmad-devel

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Traverso is a free, cross platform multitrack audio recording and editing suite,
with an innovative and easy to master User Interface. It's suited for both
the professional and home user, who needs a robust and solid DAW.

%prep
%setup -q
chmod -x ChangeLog INSTALL TODO

%build
%cmake -DWANT_MP3_DECODE=ON \
       -DWANT_MP3_ENCODE=OFF \
       -DWANT_OPENGL=ON \
       -DWANT_PORTAUDIO=ON 
%make

%install
install -D -m 0755 build/bin/%{name} %{buildroot}%{_bindir}/%{name}
install -D -m 0755 resources/images/traverso-logo.svg %{buildroot}%{_datadir}/pixmaps/%{name}.svg
install -D -m 0755 %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYRIGHT ChangeLog HISTORY README TODO
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.svg
