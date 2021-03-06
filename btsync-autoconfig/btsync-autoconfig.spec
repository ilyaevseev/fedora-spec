Name:           btsync-autoconfig
Version:        2.0.0
Release:        1%{?dist}
Summary:        Automatically create btsync config file skeletons for users

Group:          -
License:        GPL2
URL:            https://github.com/emlun/btsync-autoconfig
Source0:        https://github.com/emlun/btsync-autoconfig/archive/%{name}-%{version}.tar.gz

BuildRequires:          systemd
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd
Requires:       btsync

BuildArch:      noarch

%description
This repository contains systemd service scripts for automatically creating
config files if needed when the btsync user service starts.


%prep
%setup -q


%build


%install
make install DESTDIR=%{buildroot}


%post
%systemd_post btsync-autoconfig.service

%preun
%systemd_preun btsync-autoconfig.service

%postun
%systemd_postun_with_restart btsync-autoconfig.service


%files
%defattr(-,root,root)
%{_datadir}/%{name}
%{_userunitdir}/btsync-autoconfig.service



%changelog

