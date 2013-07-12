Summary:	D-Bus interface for user accounts management
Name:		accountsservice
Version:	0.6.34
Release:	1
License:	GPL v3
Group:		Applications/System
Source0:	http://cgit.freedesktop.org/accountsservice/snapshot/%{name}-%{version}.tar.xz
# Source0-md5:	4c37d9c9dca6275286565c194c88a265
URL:		http://cgit.freedesktop.org/accountsservice/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	pkg-config
BuildRequires:	polkit-devel
BuildRequires:	systemd-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	systemd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/accounts-service

%description
The AccountsService project provides:
- A set of D-Bus interfaces for querying and manipulating user account
  information.
- An implementation of these interfaces based on the usermod(8),
  useradd(8) and userdel(8) commands.

%package libs
Summary:	accountsservice library
Group:		Libraries

%description libs
accountsservice library.

%package devel
Summary:	accountsservice includes, and more
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
accountsservice includes, and more

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__gtkdocize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static	\
	--enable-systemd	\
	--with-systemdsystemunitdir=%{systemdunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang accounts-service

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post accounts-daemon.service

%preun
%systemd_preun accounts-daemon.service

%postun
%systemd_postun

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f accounts-service.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/accounts-daemon
/etc/dbus-1/system.d/org.freedesktop.Accounts.conf
%{systemdunitdir}/accounts-daemon.service
%{_datadir}/dbus-1/system-services/org.freedesktop.Accounts.service
%{_datadir}/polkit-1/actions/org.freedesktop.accounts.policy
%dir /var/lib/AccountsService
%dir /var/lib/AccountsService/icons
%dir /var/lib/AccountsService/users

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libaccountsservice.so.?
%attr(755,root,root) %{_libdir}/libaccountsservice.so.*.*.*
%{_libdir}/girepository-1.0/AccountsService-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaccountsservice.so
%{_includedir}/accountsservice-1.0
%{_pkgconfigdir}/accountsservice.pc
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.User.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.xml
%{_datadir}/gir-1.0/AccountsService-1.0.gir
%{_datadir}/vala/vapi/accountsservice.deps
%{_datadir}/vala/vapi/accountsservice.vapi

