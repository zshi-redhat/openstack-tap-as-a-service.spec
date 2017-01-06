%global pypi_name tap-as-a-service
%global sname neutron_taas
%global servicename neutron-taas
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Tap-as-a-Service (TaaS) is an extension to the OpenStack network service (Neutron), it provides remote port mirroring capability for tenant virtual networks.

License:        ASL 2.0
URL:            https://github.com/openstack/tap-as-a-service
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
Source1:        %{servicename}-openvswitch-agent.service
BuildArch:      noarch

BuildRequires:  python-coverage
BuildRequires:  python-hacking
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslotest
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-subunit
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python2-devel
BuildRequires:  systemd-units

%description
Tap-as-a-Service (TaaS) is an extension to the OpenStack network service (Neutron),
it provides remote port mirroring capability for tenant virtual networks.

%package -n     python2-%{pypi_name}
Summary:        An extension to the OpenStack network service(Neutron) for port mirroring
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python-pbr >= 1.6
Requires:       python-babel >= 2.3.4
Requires:       python-neutron-lib >= 0.0.3
Requires:       python-oslo-db >= 4.1.0
Requires:       python-oslo-config >= 2:3.9.0
Requires:       python-oslo-concurrency >= 3.5.0
Requires:       python-oslo-log >= 1.14.0
Requires:       python-oslo-messaging >= 4.5.0
Requires:       python-oslo-service >= 1.0.0
Requires:       python-setuptools
Requires:       openstack-neutron-common

%description -n python2-%{pypi_name}
Tap-as-a-Service (TaaS) is an extension to the OpenStack network service (Neutron),
it provides remote port mirroring capability for tenant virtual networks.

%package -n python-%{pypi_name}-doc
Summary:        Tap-as-a-service documentation
%description -n python-%{pypi_name}-doc
Documentation for Tap-as-a-service

%package -n python-%{pypi_name}-tests
Summary:        tap-as-a-service tests
Requires:       python-hacking >= 0.10.0
Requires:       python-coverage >= 4.0
Requires:       python-subunit >= 0.0.18
Requires:       python-sphinx >= 1.2.1
Requires:       python-oslo-sphinx >= 4.7.0
Requires:       python-oslotest >= 1.10.0
Requires:       python-testrepository >= 0.0.18
Requires:       python-testresources >= 0.2.4
Requires:       python-testscenarios >= 0.4
Requires:       python-testtools >= 1.4.0

%description -n python-%{pypi_name}-tests
Tap-as-a-service set of tests

%package -n %{servicename}-openvswitch-agent
Summary:        Neutron Taas openvswitch agent
%description -n %{servicename}-openvswitch-agent
Agent that enables taas functionality

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
# generate html docs
#%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py2_install

install -d -m 755 %{buildroot}/%{_sysconfdir}/neutron/
cp etc/*.ini %{buildroot}/%{_sysconfdir}/neutron/

# Make sure neutron-server loads new configuration file
install -d -m 755 %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/taas_plugin.ini %{buildroot}/%{_datadir}/neutron/server/taas_plugin.ini

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{servicename}-openvswitch-agent.service

%post
%systemd_post %{servicename}-openvswitch-agent.service

%preun
%systemd_preun %{servicename}-openvswitch-agent.service

%postun
%systemd_postun_with_restart %{servicename}-openvswitch-agent.service

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sname}
%{python2_sitelib}/tap_as_a_service-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas_plugin.ini
%{_datadir}/neutron/server/taas_plugin.ini
%exclude %{python2_sitelib}/%{sname}/tests
%exclude %{_unitdir}/%{servicename}-openvswitch-agent.service
%exclude %{_bindir}/neutron-taas-openvswitch-agent

%files -n python-%{pypi_name}-doc
%license LICENSE
%doc README.rst

%files -n python-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/%{sname}/tests

%files -n %{servicename}-openvswitch-agent
%license LICENSE
%{_unitdir}/%{servicename}-openvswitch-agent.service
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas.ini
%{_bindir}/neutron-taas-openvswitch-agent

%changelog
* Tue Jan 3 2017 Zenghui Shi <zshi@redhat.com> - 0.0.1-146
- Initial package.
