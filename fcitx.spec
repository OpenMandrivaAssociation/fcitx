%define	version	3.5
%define rel 2
%define codename BlackFri

# NOTE: set prerelease to 0 for official releases, 1 for pre-releases
%define prerelease 0

%if %prerelease
%define pre_version 070713
%define release	%mkrel -c %{pre_version} %{rel}
%else
%define release %mkrel %{rel}
%endif

Summary:	Fcitx - Free Chinese Input Toys for X
Name:		fcitx
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Internationalization
URL:		http://fcitx.redv.com
Source0:	%{name}-%{version}-%{codename}.tar.bz2
Source1:	%{name}.README.bz2
Patch0:		fcitx-3.5-fix-asneeded.patch
Patch1:		%{name}-3.2-winposition.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libx11-devel libxft-devel xpm-devel
Requires:	locales-zh

%description
%{name} is an X input method allowing people to enter simplified Chinese
characters in X environment following XIM standard.

%prep
%setup -q
%patch0 -p1
%patch1 -p0 -b .mainwin-position
bzcat %{SOURCE1} > README.mandriva

chmod 0644 doc/*

%build
sh autogen.sh
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.mandriva
%attr(0644,-,-) %doc doc/*.txt doc/*.pdf doc/*.htm doc/*.odt
%{_bindir}/*
%{_datadir}/%{name}
