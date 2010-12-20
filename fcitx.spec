%define	version 4.0.1
%define rel 1

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
Source0:	http://fcitx.googlecode.com/files/%name-%{version}_all.tar.gz
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libx11-devel
BuildRequires:	libxft-devel
BuildRequires:	xpm-devel
BuildRequires:	libxext-devel
BuildRequires:	dbus-devel
BuildRequires:	wget
BuildRequires:	cairo-devel
BuildRequires:	pango-devel
BuildRequires:	intltool
Requires:	locales-zh

%description
%{name} is an X input method allowing people to enter simplified Chinese
characters in X environment following XIM standard.

%package devel
Summary: fcitx development library
Group: Development/C
Requires: %{name} = %{version}

%description devel
fcitx development files.

%prep
%setup -q -n %name-%version

%build
%configure2_5x --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %name

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(-,root,root)
%attr(0644,-,-) %doc doc/*.txt doc/*.htm
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
