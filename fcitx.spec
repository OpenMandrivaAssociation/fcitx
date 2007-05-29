%define	version	3.5
%define rel 1

# NOTE: set prerelease to 0 for official releases, 1 for pre-releases
%define prerelease 1

%if %prerelease
%define pre_version 070528
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
URL:		http://www.fcitx.org/
%if %prerelease
Source0:	%{name}-%{version}-%{pre_version}.tar.bz2
%else
Source0:	%{name}-%{version}.tar.bz2
%endif
Source1:	%{name}.README.bz2
Patch1:		%{name}-3.2-winposition.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	automake1.8
BuildRequires:	gettext-devel
BuildRequires:	X11-devel
Requires:	locales-zh

%description
%{name} is an X input method allowing people to enter simplified Chinese
characters in X environment following XIM standard.

%prep
%setup -q
aclocal-1.9 
%patch1 -p0 -b .mainwin-position

chmod 0644 doc/*

%configure2_5x

bzcat %{SOURCE1} > README.mandrake

%build
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.mandrake
%attr(0644,-,-) %doc doc/*.txt doc/*.pdf doc/*.htm doc/*.odt
%{_bindir}/*
%{_datadir}/%{name}
