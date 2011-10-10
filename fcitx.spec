%define	version 4.1.2
%define rel 1

# NOTE: set prerelease to 0 for official releases, 1 for pre-releases
%define prerelease 0

%if %{prerelease}
%define release	%mkrel -c %{prerelease} %{rel}
%define tarballver %{version}-%{prerelease}
%else
%define release %mkrel %{rel}
%define tarballver %{version}
%endif

Summary:	Fcitx - Free Chinese Input Toys for X
Name:		fcitx
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Internationalization
URL:		http://code.google.com/p/fcitx/
Source0:	http://fcitx.googlecode.com/files/%name-%{version}_all.tar.bz2
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	automake
BuildRequires:	cmake
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
BuildRequires:	dbus-glib-devel
BuildRequires:	gtk+2-devel
%if %mdvver >= 201100
BuildRequires:	opencc-devel
%endif
BuildRequires:	chrpath
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

%package gtk
Summary: fcitx gtk module
Group: System/Internationalization
Requires: %{name} = %{version}
Requires(post): gtk+2.0
Requires(postun): gtk+2.0

%description gtk
fcitx gtk module.

%post gtk
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%{_lib}

%postun gtk
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%{_lib}

%prep
%setup -q -n %{name}-%{version}

%build
#Don't build GTK3 module because we don't have GTK3 yet
%cmake -DENABLE_GTK2_IM_MODULE=ON -DENABLE_GTK3_IM_MODULE=OFF -DCMAKE_SKIP_RPATH=OFF
%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

chrpath -d %{buildroot}%{_libdir}/*.so

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%attr(0644,-,-) %doc doc/*.txt doc/*.htm
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/x-fskin.xml
%{_iconsdir}/*/*/*/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/cmake/%{name}

%files gtk
%defattr(-,root,root)
%{_libdir}/gtk-2.0/*/immodules/im-fcitx.so