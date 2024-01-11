%if 0%{?fedora} >= 13
%global with_python3 1
%else
%if 0%{?rhel} >= 7
%global with_python3 1
%endif
%endif

%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

Name:           python-httplib2
Version:        0.10.3
Release:        4%{?dist}
Summary:        A comprehensive HTTP client library
Group:          System Environment/Libraries
License:        MIT
URL:            https://pypi.python.org/pypi/httplib2
Source0:        https://pypi.python.org/packages/source/h/httplib2/httplib2-%{version}.tar.gz
# See also the 'locater plugin' system httplib2 now allows, and
# https://github.com/dreamhost/httplib2-ca_certs_locater
# It's kind of problematic, though: https://github.com/jcgregorio/httplib2/issues/293
Patch1:         %{name}.certfile.patch
Patch2:         %{name}.getCertHost.patch
Patch3:         %{name}.rfc2459.patch
#
# Fix proxy with plain http
# https://bugzilla.redhat.com/show_bug.cgi?id=857514
# https://github.com/jcgregorio/httplib2/issues/228
# 
Patch4:         python-httplib2-0.9-proxy-http.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{with python2}
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
%endif # with python2
BuildArch:      noarch

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif # if with_python3

%global _description\
A comprehensive HTTP client library that supports many features left out of\
other HTTP libraries.

%description %_description

%if %{with python2}
%package -n python2-httplib2
Summary: %summary
%{?python_provide:%python_provide python2-httplib2}

%description -n python2-httplib2 %_description
%endif # with python2

%if 0%{?with_python3}
%package -n python3-httplib2
Summary:        A comprehensive HTTP client library
%{?python_provide:%python_provide python3-httplib2}

%description -n python3-httplib2
A comprehensive HTTP client library that supports many features left out of
other HTTP libraries.
%endif # with_python3

%prep
%setup -q -n httplib2-%{version}
%patch1 -p1 -b .certfile
%patch2 -p0 -b .getCertHost
%patch3 -p0 -b .rfc2459
%patch4 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'
%endif # with_python3

%build
%if %{with python2}
%py2_build
%endif # with python2

%if 0%{?with_python3}
pushd %{py3dir}
%py3_build
popd
%endif # with_python3

%install
%if %{with python2}
%py2_install
%endif # with python2

%if 0%{?with_python3}
pushd %{py3dir}
%py3_install
popd
%endif # with_python3

%if %{with python2}
%files -n python2-httplib2
%{python2_sitelib}/*
%endif # with python2

%if 0%{?with_python3}
%files -n python3-httplib2
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Fri Jun 08 2018 Charalampos Stratakis <cstratak@redhat.com> - 0.10.3-4
- Conditionalize the python2 subpackage

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Nick Bebout <nb@fedoraproject.org> - 0.10.3-2
- Fix BuildRequires to use python2-* instead of python-*

* Sun Sep 10 2017 Nick Bebout <nb@fedoraproject.org> - 0.10.3-1
- Update to 0.10.3

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9.2-7
- Python 2 binary package renamed to python2-httplib2
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.2-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 26 2015 Kevin Fenzi <kevin@scrye.com> - 0.9.2-1
- Update to 0.9.2

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 12 2015 Kevin Fenzi <kevin@scrye.com> 0.9.1-1
- Update to 0.9.1 and drop upstreamed patches

* Fri Apr 03 2015 Kevin Fenzi <kevin@scrye.com> 0.9-6
- Add patch to fix http over proxy. Fixes bug #857514
- Add patch to fix CVE-2013-2037. Fixes bug #958640
- Add patch to fix binary headers in python3. Fixes bug #1205127

* Mon Jan 12 2015 Adam Williamson <awilliam@redhat.com> - 0.9-5
- certfile.patch: use /etc/pki/tls not /etc/ssl/certs, patch python3 too

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 0.9-4
- Replace python-setuptools-devel BR with python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri May 23 2014 Kevin Fenzi <kevin@scrye.com> 0.9-1
- Update to 0.9

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.7-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Ding-Yi Chen <dchen at redhat.com> - 0.7.7-1
- Upstream update to 0.7.7

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.7.4-7
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Jul 27 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.4-6
- Fixed Bug 840968 - SSL errors when the site certificate contains
  subjectAltName but DNS is not in it

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.4-4
- Unify the spec file between EPEL and Fedora.

* Thu Jun 21 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.4-3
- Applied patch suggested by richardfearn@gmail.com regarding issue 208
- Fixed: Bug 832344 - Certification validation fails due to multiple 'dns' entries in subjectAltName

* Fri Jun 01 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.4-2
- Upstream update for Fedora

* Thu May 03 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.4-1
- Upstream update to 0.7.4
- Applied patch suggested in issue 208

* Fri Feb 24 2012 Ding-Yi Chen <dchen at redhat.com> - 0.7.2-1
- Upstream update to 0.7.2
  Which may fixed http://code.google.com/p/httplib2/issues/detail?id=62
  Note this version uses fedora's cert file bundle instead of httplib2
  default.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 29 2011 Ding-Yi Chen <dchen at redhat.com>  - 0.4.0-5.el6
- Apply that address python-httplib2 (GoogleCode Hosted) issue 39
  http://code.google.com/p/httplib2/issues/detail?id=39

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.0-4
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 20 2010 Tom "spot" Callaway <tcallawa@redhat.com>
- minor spec cleanups
- enable python3 support

* Fri Apr 02 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 0.6.0-1
- version upgrade (#566721)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4.0-2
- Rebuild for Python 2.6

* Thu Dec 27 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 0.4.0-1
- initial version
