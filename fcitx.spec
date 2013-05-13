Name:		fcitx
Version:	4.2.2
Release:	2
Summary:	Fcitx - Free Chinese Input Toys for X
License:	GPLv2
Group:		System/Internationalization
URL:		http://code.google.com/p/fcitx/
Source0:	http://fcitx.googlecode.com/files/%{name}-%{version}_dict.tar.xz
BuildRequires:	automake
BuildRequires:	cmake
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xft)
BuildRequires:	xpm-devel
BuildRequires:	pkgconfig(xext)
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


%changelog
* Thu Apr 26 2012 Alexander Khrukin <akhrukin@mandriva.org> 4.2.2-1
+ Revision: 793520
- version update 4.2.2

* Tue Mar 20 2012 Andrey Bondrov <abondrov@mandriva.org> 4.2.1-1
+ Revision: 785795
- New version 4.2.1

* Mon Oct 10 2011 Andrey Bondrov <abondrov@mandriva.org> 4.1.2-1
+ Revision: 703989
- New version 4.1.2, new subpackage gtk, more BR

* Mon Dec 20 2010 Funda Wang <fwang@mandriva.org> 4.0.1-1mdv2011.0
+ Revision: 623234
- new version 4.0.1

* Sun Nov 21 2010 Funda Wang <fwang@mandriva.org> 4.0.0-2mdv2011.0
+ Revision: 599321
- add two upstream patch to fix problems

* Fri Nov 19 2010 Funda Wang <fwang@mandriva.org> 4.0.0-1mdv2011.0
+ Revision: 598900
- new version 4.0.0
- new version 4.0.0

* Fri Feb 19 2010 Funda Wang <fwang@mandriva.org> 3.6.3-1mdv2010.1
+ Revision: 507965
- BR dbus
- new version 3.6.3

* Fri Nov 06 2009 Funda Wang <fwang@mandriva.org> 3.6.2-1mdv2010.1
+ Revision: 460569
- New version 3.6.2

* Mon Oct 05 2009 Funda Wang <fwang@mandriva.org> 3.6.1-2mdv2010.0
+ Revision: 454166
- update to svn trunk
- really use 3.6.1 tarball

* Thu Sep 24 2009 Frederik Himpe <fhimpe@mandriva.org> 3.6.1-1mdv2010.0
+ Revision: 448396
- update to new version 3.6.1

* Sat Jul 11 2009 Funda Wang <fwang@mandriva.org> 3.6.0-1mdv2010.0
+ Revision: 394836
- BR xext
- fix linkage
- new version 3.6.0 final

* Sun Jan 18 2009 Funda Wang <fwang@mandriva.org> 3.6.0-0.rc.1mdv2009.1
+ Revision: 330812
- New version 3.6.0 rc
- rediff winposition patch

* Thu Jun 19 2008 Funda Wang <fwang@mandriva.org> 3.5-2mdv2009.0
+ Revision: 226418
- add patch for -asneeded
- simplify the BR

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 3.5-1mdv2008.1
+ Revision: 136411
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - s/Mandrake/Mandriva/

* Thu Jul 19 2007 Funda Wang <fwang@mandriva.org> 3.5-1mdv2008.0
+ Revision: 53434
- New version

* Fri Jul 06 2007 Funda Wang <fwang@mandriva.org> 3.5-0.070703.1mdv2008.0
+ Revision: 49152
- New version

* Sun Jul 01 2007 Funda Wang <fwang@mandriva.org> 3.5-0.070630.1mdv2008.0
+ Revision: 46417
- New version

* Tue May 29 2007 Funda Wang <fwang@mandriva.org> 3.5-0.070528.1mdv2008.0
+ Revision: 32415
- New snapshot

* Mon May 28 2007 Funda Wang <fwang@mandriva.org> 3.5-0.070527.1mdv2008.0
+ Revision: 31890
- New version

* Mon May 07 2007 Funda Wang <fwang@mandriva.org> 3.5-0.070507.1mdv2008.0
+ Revision: 24113
- New upstream version 070507

