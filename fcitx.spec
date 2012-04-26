Name:		fcitx
Version:	4.2.2
Release:	1
Summary:	Fcitx - Free Chinese Input Toys for X
License:	GPLv2
Group:		System/Internationalization
URL:		http://code.google.com/p/fcitx/
Source0:	http://fcitx.googlecode.com/files/%{name}-%{version}_dict.tar.xz
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
BuildRequires:	gtk+3-devel

%if %mdvver >= 201100
BuildRequires:	opencc-devel
%endif
BuildRequires:	chrpath
Requires:	locales-zh

%description
%{name} is an X input method allowing people to enter simplified Chinese
characters in X environment following XIM standard.

%package devel
Summary:	fcitx development library
Group:		Development/C
Requires:	%{name} = %{version}

%description devel
fcitx development files.

%package gtk
Summary:	fcitx gtk module
Group:		System/Internationalization
Requires:	%{name} = %{version}
Requires(post):	gtk+2.0
Requires(postun): gtk+2.0

%description gtk
fcitx gtk module.

%post gtk
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%{_lib}

%postun gtk
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%{_lib}

%prep
%setup -q

%build
#Don't build GTK3 module because we don't have GTK3 yet
%cmake -DENABLE_GTK2_IM_MODULE=ON -DENABLE_GTK3_IM_MODULE=ON -DCMAKE_SKIP_RPATH=OFF
%make

%install
%makeinstall_std -C build

chrpath -d %{buildroot}%{_libdir}/*.so

%find_lang %{name}

%files -f %{name}.lang
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
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/cmake/%{name}

%files gtk
%{_libdir}/gtk-2.0/*/immodules/im-fcitx.so
%{_libdir}/gtk-3.0/*/immodules/im-fcitx.so
