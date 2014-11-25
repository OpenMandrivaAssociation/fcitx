# Whether or not to build Qt 4.x input module
%bcond_without qt4
# Whether or not to build GTK 2.x input module
%bcond_without gtk2
# Whether or not to build GTK 3.x input module
%bcond_without gtk3
# Whether or not to build the Classic UI (not needed with kimpanel)
%bcond_without classic_ui

Name:		fcitx
Version:	4.2.8.4
Release:	8
Summary:	Fcitx - Free Chinese Input Tool for X
License:	GPLv2
Group:		System/Internationalization
URL:		http://www.fcitx-im.org/
Source0:	http://download.fcitx-im.org/fcitx/%{name}-%{version}_dict.tar.xz
Source100:	%{name}.rpmlintrc
Patch0:		fcitx-4.2.8.1-defaults.patch
BuildRequires:	automake
BuildRequires:	cmake
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	wget
BuildRequires:	intltool
BuildRequires:	pkgconfig(opencc)
BuildRequires:	chrpath
Requires:	locales-zh

%description
%{name} is an X input method allowing people to enter simplified Chinese
characters in X environment following XIM standard.

%package devel
Summary:	Fcitx development library
Group:		Development/C
Requires:	%{name} = %{version}

%description devel
fcitx development files.

%if %{with classic_ui}
%package ui
Summary:	Classic UI for fcitx
Group:		System/Internationalization
Requires:	%{name} = %{EVRD}
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(pango)

%description ui
Classic UI for fcitx.

This is needed if you don't use kimpanel.
%endif

%if %{with qt4}
%package qt4
Summary:	Fcitx Qt 4.x module
Group:		System/Internationalization
Requires:	%{name} = %{EVRD}
BuildRequires:	pkgconfig(QtCore) pkgconfig(QtGui) pkgconfig(QtDBus)
Requires:	plasma-applet-kimpanel plasma-dataengine-kimpanel

%description qt4
fcitx Qt 4.x module.
%endif

%package configtool
Summary:	Tool for configuring fcitx
Group:		System/Internationalization
Requires:	%{name} = %{EVRD}

%description configtool
Tool for configuring fcitx

%if %{with gtk2} || %{with gtk3}
%package gtk
Summary:	Common files for the fcitx gtk 2.x and 3.x modules
Group:		System/Internationalization
Requires:	%{name} = %{EVRD}
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(dbus-glib-1)

%description gtk
Common files for the fcitx gtk 2.x and 3.x modules
%endif

%if %{with gtk2}
%package gtk2
Summary:	Fcitx gtk 2.x module
Group:		System/Internationalization
BuildRequires:	pkgconfig(gtk+-x11-2.0)
Requires:	%{name}-gtk = %{EVRD}
Requires(post):	gtk+2.0
Requires(postun): gtk+2.0

%description gtk2
fcitx gtk module.

%post gtk2
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%{_lib}

%postun gtk2
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%{_lib}
%endif

%if %{with gtk3}
%package gtk3
Summary:	Fcitx gtk 3.x module
Group:		System/Internationalization
Requires:	%{name} = %{version}
Requires:	%{name}-gtk = %{EVRD}
BuildRequires:	pkgconfig(gtk+-x11-3.0)

%description gtk3
fcitx gtk module.
%endif

%prep
%setup -q
%apply_patches

%build
%cmake -DCMAKE_SKIP_RPATH=OFF \
	-DENABLE_GTK2_IM_MODULE=%{with gtk2} \
	-DENABLE_GTK3_IM_MODULE=%{with gtk3} \
	-DENABLE_QT_IM_MODULE=%{with qt4} \
	-DENABLE_CAIRO=%{with classic_ui} \
	-DENABLE_PANGO=%{with classic_ui}
%make

%install
%makeinstall_std -C build

chrpath -d %{buildroot}%{_libdir}/*.so

# A hack - make install issue?
mkdir -p %{buildroot}/etc/xdg/autostart/
mv %{buildroot}/usr/etc/xdg/autostart/* %{buildroot}/etc/xdg/autostart/
rm -rf %{buildroot}/usr/etc

%if %{without classic_ui}
# Built even without classic_ui... But apparently not needed
rm -rf %{buildroot}%{_datadir}/fcitx/skin
%endif

%find_lang %{name}

%files -f %{name}.lang
%attr(0644,-,-) %doc doc/*.txt doc/*.htm
%{_bindir}/createPYMB
%{_bindir}/fcitx
%{_bindir}/fcitx-autostart
%{_bindir}/fcitx-dbus-watcher
%{_bindir}/fcitx-diagnose
%{_bindir}/fcitx-remote
%{_bindir}/mb2org
%{_bindir}/mb2txt
%{_bindir}/readPYBase
%{_bindir}/readPYMB
%{_bindir}/scel2org
%{_bindir}/txt2mb
%{_libdir}/libfcitx-config.so.4*
%{_libdir}/libfcitx-core.so.0*
%{_libdir}/libfcitx-utils.so.0*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/fcitx-autoeng.so
%{_libdir}/%{name}/fcitx-chttrans.so
%{_libdir}/%{name}/fcitx-clipboard.so
%{_libdir}/%{name}/fcitx-dbus.so
%{_libdir}/%{name}/fcitx-freedesktop-notify.so
%{_libdir}/%{name}/fcitx-fullwidth-char.so
%{_libdir}/%{name}/fcitx-imselector.so
%{_libdir}/%{name}/fcitx-ipc.so
%{_libdir}/%{name}/fcitx-keyboard.so
%{_libdir}/%{name}/fcitx-notificationitem.so
%{_libdir}/%{name}/fcitx-pinyin-enhance.so
%{_libdir}/%{name}/fcitx-pinyin.so
%{_libdir}/%{name}/fcitx-punc.so
%{_libdir}/%{name}/fcitx-quickphrase.so
%{_libdir}/%{name}/fcitx-qw.so
%{_libdir}/%{name}/fcitx-remote-module.so
%{_libdir}/%{name}/fcitx-spell.so
%{_libdir}/%{name}/fcitx-table.so
%{_libdir}/%{name}/fcitx-unicode.so
%{_libdir}/%{name}/fcitx-x11.so
%{_libdir}/%{name}/fcitx-xim.so
%{_libdir}/%{name}/fcitx-xkb.so
%{_libdir}/%{name}/fcitx-xkbdbus.so
%dir %{_libdir}/%{name}/libexec
%{_libdir}/%{name}/libexec/comp-spell-dict
%{_libdir}/%{name}/libexec/fcitx-po-parser
%{_libdir}/%{name}/libexec/fcitx-scanner
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/addon
%{_datadir}/%{name}/addon/fcitx-autoeng.conf
%{_datadir}/%{name}/addon/fcitx-chttrans.conf
%{_datadir}/%{name}/addon/fcitx-clipboard.conf
%{_datadir}/%{name}/addon/fcitx-dbus.conf
%{_datadir}/%{name}/addon/fcitx-freedesktop-notify.conf
%{_datadir}/%{name}/addon/fcitx-fullwidth-char.conf
%{_datadir}/%{name}/addon/fcitx-imselector.conf
%{_datadir}/%{name}/addon/fcitx-ipc.conf
%{_datadir}/%{name}/addon/fcitx-keyboard.conf
%{_datadir}/%{name}/addon/fcitx-notificationitem.conf
%{_datadir}/%{name}/addon/fcitx-pinyin-enhance.conf
%{_datadir}/%{name}/addon/fcitx-pinyin.conf
%{_datadir}/%{name}/addon/fcitx-punc.conf
%{_datadir}/%{name}/addon/fcitx-quickphrase.conf
%{_datadir}/%{name}/addon/fcitx-qw.conf
%{_datadir}/%{name}/addon/fcitx-remote-module.conf
%{_datadir}/%{name}/addon/fcitx-spell.conf
%{_datadir}/%{name}/addon/fcitx-table.conf
%{_datadir}/%{name}/addon/fcitx-unicode.conf
%{_datadir}/%{name}/addon/fcitx-x11.conf
%{_datadir}/%{name}/addon/fcitx-xim.conf
%{_datadir}/%{name}/addon/fcitx-xkb.conf
%{_datadir}/%{name}/addon/fcitx-xkbdbus.conf
%dir %{_datadir}/%{name}/configdesc
%{_datadir}/%{name}/configdesc/addon.desc
%{_datadir}/%{name}/configdesc/config.desc
%{_datadir}/%{name}/configdesc/fcitx-autoeng.desc
%{_datadir}/%{name}/configdesc/fcitx-chttrans.desc
%{_datadir}/%{name}/configdesc/fcitx-clipboard.desc
%{_datadir}/%{name}/configdesc/fcitx-imselector.desc
%{_datadir}/%{name}/configdesc/fcitx-keyboard.desc
%{_datadir}/%{name}/configdesc/fcitx-pinyin.desc
%{_datadir}/%{name}/configdesc/fcitx-pinyin-enhance.desc
%{_datadir}/%{name}/configdesc/fcitx-quickphrase.desc
%{_datadir}/%{name}/configdesc/fcitx-spell.desc
%{_datadir}/%{name}/configdesc/fcitx-table.desc
%{_datadir}/%{name}/configdesc/fcitx-unicode.desc
%{_datadir}/%{name}/configdesc/fcitx-xim.desc
%{_datadir}/%{name}/configdesc/fcitx-xkb.desc
%{_datadir}/%{name}/configdesc/inputmethod.desc
%{_datadir}/%{name}/configdesc/profile.desc
%{_datadir}/%{name}/configdesc/table.desc
%dir %{_datadir}/%{name}/data
%{_datadir}/%{name}/data/AutoEng.dat
%{_datadir}/%{name}/data/charselectdata
%{_datadir}/%{name}/data/gbks2t.tab
%{_datadir}/%{name}/data/punc.mb.zh_CN
%{_datadir}/%{name}/data/punc.mb.zh_HK
%{_datadir}/%{name}/data/punc.mb.zh_TW
%{_datadir}/%{name}/data/vk.conf
%dir %{_datadir}/%{name}/data/quickphrase.d
%{_datadir}/%{name}/data/quickphrase.d/emoji.mb
%{_datadir}/%{name}/data/quickphrase.d/latex.mb
%dir %{_datadir}/%{name}/dbus
%{_datadir}/%{name}/dbus/daemon.conf
%dir %{_datadir}/%{name}/imicon
%{_datadir}/%{name}/imicon/*
%dir %{_datadir}/%{name}/inputmethod
%{_datadir}/%{name}/inputmethod/pinyin.conf
%{_datadir}/%{name}/inputmethod/qw.conf
%{_datadir}/%{name}/inputmethod/shuangpin.conf
%dir %{_datadir}/%{name}/pinyin
%{_datadir}/%{name}/pinyin/*
%dir %{_datadir}/%{name}/py-enhance
%{_datadir}/%{name}/py-enhance/*
%{_mandir}/man1/createPYMB.1*
%{_mandir}/man1/fcitx-remote.1*
%{_mandir}/man1/fcitx.1*
%{_mandir}/man1/mb2org.1*
%{_mandir}/man1/mb2txt.1*
%{_mandir}/man1/readPYBase.1*
%{_mandir}/man1/readPYMB.1*
%{_mandir}/man1/scel2org.1*
%{_mandir}/man1/txt2mb.1*
%{_datadir}/applications/fcitx.desktop
%{_datadir}/icons/hicolor/*/*/fcitx*.*
%{_sysconfdir}/xdg/autostart/fcitx-autostart.desktop
%dir %{_datadir}/fcitx/spell
%{_datadir}/fcitx/spell/*
%dir %{_datadir}/fcitx/table
%{_datadir}/fcitx/table/*
%dir %{_datadir}/fcitx/data
%{_datadir}/fcitx/data/*
%{_datadir}/dbus-1/services/*service

%files devel
%{_bindir}/fcitx4-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/cmake/%{name}

%if %{with qt4}
%files qt4
%{_libdir}/fcitx/libexec/fcitx-qt-gui-wrapper
%{_libdir}/qt4/plugins/inputmethods/qtim-fcitx.so
%{_libdir}/%{name}/fcitx-kimpanel-ui.so
%{_datadir}/%{name}/addon/fcitx-kimpanel-ui.conf
%{_libdir}/%{name}/qt
%{_libdir}/libfcitx-qt.so.0*
%endif

%if %{with gtk2} || %{with gtk3}
%files gtk
%{_libdir}/girepository-1.0/Fcitx-1.0.typelib
%{_datadir}/gir-1.0/Fcitx-1.0.gir
%{_libdir}/libfcitx-gclient.so.0*
%endif

%if %{with gtk2}
%files gtk2
%{_libdir}/gtk-2.0/*/immodules/im-fcitx.so
%endif

%if %{with gtk3}
%files gtk3
%{_libdir}/gtk-3.0/*/immodules/im-fcitx.so
%endif

%if %{with classic_ui}
%files ui
%{_bindir}/fcitx-skin-installer
%{_libdir}/fcitx/fcitx-classic-ui.so
%{_libdir}/fcitx/fcitx-vk.so
%{_datadir}/applications/fcitx-skin-installer.desktop
%{_datadir}/fcitx/addon/fcitx-classic-ui.conf
%{_datadir}/fcitx/addon/fcitx-vk.conf
%{_datadir}/fcitx/configdesc/fcitx-classic-ui.desc
%{_datadir}/fcitx/configdesc/skin.desc
%{_datadir}/mime/packages/x-fskin.xml
%{_datadir}/fcitx/skin
%endif

%files configtool
%{_bindir}/fcitx-configtool
%{_datadir}/applications/fcitx-configtool.desktop
