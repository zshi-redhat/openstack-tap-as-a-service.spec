%global pypi_name tap-as-a-service
%global sname neutron_taas
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Tap-as-a-Service (TaaS) is an extension to the OpenStack network service (Neutron), it provides remote port mirroring capability for tenant virtual networks.

License:        ASL 2.0
URL:            https://github.com/openstack/tap-as-a-service
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

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

%description
Tap-as-a-Service (TaaS) is an extension to the OpenStack network service (Neutron),
it provides remote port mirroring capability for tenant virtual networks.

%package -n     python2-%{pypi_name}
Summary:        An extension to the OpenStack network service(Neutron) for port mirroring
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python-pbr >= 1.6
Requires:       python-babel >= 2.3.4
Requires:       python-neutron-lib >= 0.1.0
Requires:       python-oslo-db >= 4.1.0
Requires:       python-oslo-config >= 2:3.9.0
Requires:       python-oslo-concurrency >= 3.5.0
Requires:       python-oslo-log >= 1.14.0
Requires:       python-oslo-messaging >= 4.5.0
Requires:       python-oslo-service >= 1.0.0
Requires:       python-setuptools

%description -n python2-%{pypi_name}
Tap-as-a-Service (TaaS) is an extension to the OpenStack network service (Neutron),
it provides remote port mirroring capability for tenant virtual networks.

%package -n python-%{pypi_name}-doc
Summary:        Tap-as-a-service documentation
%description -n python-%{pypi_name}-doc
Documentation for Tap-as-a-service

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


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sname}
%{python2_sitelib}/tap_as_a_service-*.egg-info
%{_bindir}/neutron-taas-openvswitch-agent

%files -n python-%{pypi_name}-doc
#%doc html
%license LICENSE

%changelog
* Tue Jan 3 2017 Zenghui Shi <zshi@redhat.com> - 0.0.1-146
- Initial package.
