%define	version	3.6.1
%define rel 2

# NOTE: set prerelease to 0 for official releases, 1 for pre-releases
%define prerelease 0

%if %prerelease
%define release	%mkrel -c %{prerelease} %{rel}
%define tarballver %version-%prerelease
%else
%define release %mkrel %{rel}
%define tarballver %version
%endif

Summary:	Fcitx - Free Chinese Input Toys for X
Name:		fcitx
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Internationalization
URL:		http://code.google.com/p/fcitx/
Source0:	http://fcitx.googlecode.com/files/%name-%version.tar.bz2
Patch0:		fcitx-3.6-fix-asneeded.patch
Patch1:		fcitx-3.6.0-winposition.patch
Patch2:		fcitx-3.6.1-r256.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libx11-devel libxft-devel xpm-devel libxext-devel
Requires:	locales-zh

%description
%{name} is an X input method allowing people to enter simplified Chinese
characters in X environment following XIM standard.

%prep
%setup -q -n %name-%version
%patch0 -p1
%patch1 -p0 -b .mainwin-position
%patch2 -p0

%build
./autogen.sh
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,-,-) %doc doc/*.txt doc/*.pdf doc/*.htm doc/*.odt
%{_bindir}/*
%{_datadir}/%{name}
