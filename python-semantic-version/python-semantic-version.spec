%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name: python-semantic-version
Version: 2.3.0
Release: 1%{?dist}
Summary: A library implementing the 'SemVer' scheme

License: BSD
URL: https://github.com/rbarrois/python-semanticversion
Source0: https://github.com/rbarrois/python-semanticversion/archive/v2.3.0.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-sphinx

# optional for unit tests
# not available in rhel6/epel
%if 0%{?fedora}
BuildRequires: python-django
BuildRequires: python-django-south
%endif

%if 0%{?rhel}
BuildRequires: python-unittest2
%endif

%if 0%{?with_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-sphinx

# optional for unit tests
BuildRequires: python3-django
# python3-django-south is not currently packaged for F19
%if 0%{?fedora} >= 20
BuildRequires: python3-django-south
%endif
%endif # if with_python3

%description
This small python library provides a few tools to handle SemVer
(http://semver.org) in Python. It follows strictly the 2.0.0 version of the
SemVer scheme.


%if 0%{?with_python3}
%package -n python3-semantic-version
Summary: A library implementing the 'SemVer' scheme.

%description -n python3-semantic-version
This small python library provides a few tools to handle SemVer
(http://semver.org) in Python. It follows strictly the 2.0.0 version of the
SemVer scheme.

This subpackage is for python3
%endif # with_python3


%prep
%setup -q -n python-semanticversion-%{version}

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif


%check
%{__python2} setup.py test

%if 0%{?with_python3}
# setup.py iterates over a file "__init__.py" in get_version(), and in that file,
# the author's name causes a UnicodeDecodeError if the locale's encoding is not
# set to UTF-8
export LC_ALL=en_US.UTF-8
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3


%build
%{__python2} setup.py build

%if 0%{?with_python3}
# setup.py iterates over a file "__init__.py" in get_version(), and in that file,
# the author's name causes a UnicodeDecodeError if the locale's encoding is not
# set to UTF-8
export LC_ALL=en_US.UTF-8
pushd %{py3dir}
python3 -c 'import locale; print(locale.getpreferredencoding(False))'
%{__python3} setup.py build
popd
%endif # with_python3


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
# setup.py iterates over a file "__init__.py" in get_version(), and in that file,
# the author's name causes a UnicodeDecodeError if the locale's encoding is not
# set to UTF-8
export LC_ALL=en_US.UTF-8
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

pushd docs && make html
popd && mv docs/_build/html htmldocs
rm -rf docs
rm -f htmldocs/.buildinfo


%files
%defattr(-,root,root,-)
%{python2_sitelib}/semantic_version
%{python2_sitelib}/semantic_version*.egg-info
%doc ChangeLog htmldocs LICENSE README.rst

%if 0%{?with_python3}
%files -n python3-semantic-version
%defattr(-,root,root,-)
%{python3_sitelib}/*
%doc ChangeLog htmldocs LICENSE README.rst
%endif # with_python3


%changelog
* Sun Mar 16 2014 Michael Hrivnak <mhrivnak@redhat.com> - 2.3.0-1
- initial packaging
