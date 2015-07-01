# turn of test suite for now, we'll reenable once the Fedora's
#  patch for skipping network tests is upstreamable and upstreamed :)
%global with_tests 0

%if 0%{?fedora}
%global with_python3 1

%if 0%{?fedora} > 20
%global build_wheel 1
%endif
%endif

%global srcname pip
%if 0%{?build_wheel}
%global python2_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
%if 0%{?with_python3}
%global python3_wheelname %python2_wheelname
%endif
%endif

Name:           python-%{srcname}
Version:        7.1.0
Release:        1%{?dist}
Summary:        A tool for installing and managing Python packages

Group:          Development/Libraries
License:        MIT
URL:            http://www.pip-installer.org
Source0:        http://pypi.python.org/packages/source/p/pip/%{srcname}-%{version}.tar.gz

Patch0:         pip-7.0-allow-stripping-prefix-from-wheel-RECORD-files.patch

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?with_tests}
BuildRequires:  python-mock
BuildRequires:  pytest
BuildRequires:  python-scripttest
BuildRequires:  python-virtualenv
%endif
%if 0%{?build_wheel}
BuildRequires:  python-pip
BuildRequires:  python-wheel
%endif
Requires:       python-setuptools

%description
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.


%if 0%{?with_python3}
%package -n python3-pip
Summary:        A tool for installing and managing Python3 packages
Group:          Development/Libraries

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?build_wheel}
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%endif
Requires:  python3-setuptools

%description -n python3-pip
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}

%patch0 -p1

%{__sed} -i '1d' pip/__init__.py

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif # with_python3


%build
%if 0%{?build_wheel}
%{__python} setup.py bdist_wheel
%else
%{__python} setup.py build
%endif

%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?build_wheel}
%{__python3} setup.py bdist_wheel
%else
%{__python3} setup.py build
%endif
popd
%endif # with_python3


%install
%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?build_wheel}
pip3 install -I dist/%{python3_wheelname} --root %{buildroot} --strip-file-prefix %{buildroot}
# TODO: we have to remove this by hand now, but it'd be nice if we wouldn't have to
# (pip install wheel doesn't overwrite)
rm %{buildroot}%{_bindir}/pip
%else
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif
%endif # with_python3

%if 0%{?build_wheel}
pip2 install -I dist/%{python2_wheelname} --root %{buildroot} --strip-file-prefix %{buildroot}
%else
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%endif

%if 0%{?with_tests}
%check
python setup.py test
%endif

%files
%doc LICENSE.txt README.rst docs
%{_bindir}/pip
%{_bindir}/pip2*
%{python_sitelib}/pip*

%if 0%{?with_python3}
%files -n python3-pip
%doc LICENSE.txt README.rst docs
%{_bindir}/pip3*
%{python3_sitelib}/pip*
%endif # with_python3

%changelog
* Wed Jul 01 2015 Donald Stufft <donald@stufft.io> - 7.1.0-1
- Update to 7.1.0

* Mon Jun 22 2015 Donald Stufft <donald@stufft.io> - 7.0.3-2
- Fix the patch so it applies cleanly against 7.0

* Mon Jun 22 2015 Donald Stufft <donald@stufft.io> - 7.0.3-1
- Update to 7.0.3

* Thu Feb 12 2015 Donald Stufft <donald@stufft.io> - 6.0.8-1
- Update to 6.0.8

* Wed Jan 28 2015 Donald Stufft <donald@stufft.io> - 6.0.7-1
- Update to 6.0.7

* Wed Jan 14 2015 Slavek Kabrda <bkabrda@redhat.com> - 6.0.6-1
- Updated to 6.0.6
- Specfile cleanup and fixes for copr pypa repo.

* Thu Dec 18 2014 Slavek Kabrda <bkabrda@redhat.com> - 1.5.6-5
- Only enable tests on Fedora.

* Mon Dec 01 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-4
- Add tests
- Add patch skipping tests requiring Internet access

* Tue Nov 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-3
- Added patch for local dos with predictable temp dictionary names
  (http://seclists.org/oss-sec/2014/q4/655)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-1
- Update to 1.5.6

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-4
- Rebuild as wheel for Python 3.4

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-3
- Disable build_wheel

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-2
- Rebuild as wheel for Python 3.4

* Mon Apr 07 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-1
- Updated to 1.5.4

* Mon Oct 14 2013 Tim Flink <tflink@fedoraproject.org> - 1.4.1-1
- Removed patch for CVE 2013-2099 as it has been included in the upstream 1.4.1 release
- Updated version to 1.4.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-4
- Fix for CVE 2013-2099

* Thu May 23 2013 Tim Flink <tflink@fedoraproject.org> - 1.3.1-3
- undo python2 executable rename to python-pip. fixes #958377
- fix summary to match upstream

* Mon May 06 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.3.1-2
- Fix main package Summary, it's for Python 2, not 3 (#877401)

* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - 1.3.1-1
- Update to 1.3.1, fix for CVE-2013-1888.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-2
- Fixing files for python3-pip

* Thu Oct 04 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-1
- Update to upstream 1.2.1
- Change binary from pip-python to python-pip (RHBZ#855495)
- Add alias from python-pip to pip-python, to be removed at a later date

* Tue May 15 2012 Tim Flink <tflink@fedoraproject.org> - 1.1.0-1
- Update to upstream 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 and added python3 subpackage

* Wed Jun 22 2011 Tim Flink <tflink@fedoraproject.org> - 0.8.3-1
- update to 0.8.3 and project home page

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Luke Macken <lmacken@redhat.com> - 0.8.2-1
- update to 0.8.2 of pip
* Mon Aug 30 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.8-1
- update to 0.8 of pip
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 7 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.2-1
- update to 0.7.2 of pip
* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.1-1
- update to 0.7.1 of pip
* Fri Jan 1 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1.4
- fix dependency issue
* Fri Dec 18 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-2
- fix spec file
* Thu Dec 17 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-1
- upgrade to 0.6.1 of pip
* Mon Aug 31 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.4-1
- Initial package

