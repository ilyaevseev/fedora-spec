# FIXME: "constraint certificate verification turned off"

%define ntpd_user openntpd
%define ntpd_group openntpd

Name:           openntpd
Version:        5.9p1
Release:        2%{?dist}
Summary:        free and easy to use implementation of the network time protocol

Group:          -
License:        BSD
URL:            http://www.openntpd.org/
Source0:        http://ftp2.eu.openbsd.org/pub/OpenBSD/OpenNTPD/%{name}-%{version}.tar.gz
Source1:        openntpd.service
Source2:        openntpd.sysconfig

BuildRequires:          systemd
Requires(pre):          shadow-utils
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd

%description
OpenNTPD is a FREE, easy to use implementation of the Network Time Protocol. It
provides the ability to sync the local clock to remote NTP servers and can act
as NTP server itself, redistributing the local clock.


%prep
%setup -q

# patch the man pages for the ntpd -> openntpd change
sed -i "s@\.Xr ntpd 8@.Xr openntpd 8@g" src/*.5 src/*.8
sed -i "s@\.Dt NTPD 8@.Dt OPENNTPD 8@g" src/ntpd.8
sed -i "s@\.Nm ntpd@.Nm openntpd@g" src/ntpd.8


%build
%configure --with-privsep-user=%{ntpd_user}
make %{?_smp_mflags}


%install
%make_install

# install service file
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/openntpd.service
install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/openntpd

# move the binary and man page for the ntpd -> openntpd change
pushd $RPM_BUILD_ROOT
mv .%{_sbindir}/{,open}ntpd
mv .%{_mandir}/man8/{,open}ntpd.8
popd


%pre
getent group %{ntpd_group} >/dev/null || groupadd -r %{ntpd_group}
getent passwd %{ntpd_user} >/dev/null || \
    useradd -r -g %{ntpd_group} -d /var/empty -s /sbin/nologin \
    -c "OpenNTP daemon" -m %{ntpd_user}
exit 0


%post
%systemd_post openntpd.service


%preun
%systemd_preun openntpd.service


%postun
%systemd_postun_with_restart openntpd.service


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/ntpd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/openntpd
%{_sbindir}/*
%{_unitdir}/openntpd.service
%doc %{_mandir}



%changelog
