%global libname solv

# number of commits since last release
%global gitnum 20
%global commit 668e2495d942e888403f47cd5ce140703a6bb3e1
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with perl_bindings
%bcond_with ruby_bindings
%bcond_with python_bindings
%if %{with python_bindings}
  %bcond_with python3
%endif
%else
%bcond_without perl_bindings
%bcond_without ruby_bindings
%bcond_without python_bindings
%if %{with python_bindings}
  %bcond_without python3
%endif
%endif
# Creates special prefixed pseudo-packages from appdata metadata
%bcond_without appdata
# Creates special prefixed "group:", "category:" pseudo-packages
%bcond_without comps
# For rich dependencies
%bcond_without complex_deps
%if 0%{?rhel}
%bcond_with helix_repo
%bcond_with suse_repo
%bcond_with debian_repo
%bcond_with arch_repo
# For handling deb + rpm at the same time
%bcond_with multi_semantics
%else
%bcond_without helix_repo
%bcond_without suse_repo
%bcond_without debian_repo
%bcond_without arch_repo
# For handling deb + rpm at the same time
%bcond_without multi_semantics
%endif

Name:           lib%{libname}
Version:        0.6.26
Release:        5%{?commit:.git.%{gitnum}.%{shortcommit}}%{?dist}
Summary:        Package dependency solver

License:        BSD
URL:            https://github.com/openSUSE/libsolv
%if %{undefined commit}
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source:         %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(rpm)
BuildRequires:  zlib-devel
# -DWITH_LIBXML2=ON
BuildRequires:  libxml2-devel
# -DFEDORA=1
# -DENABLE_RPMDB=ON
BuildRequires:  libdb-devel
# -DENABLE_LZMA_COMPRESSION=ON
BuildRequires:  xz-devel
# -DENABLE_BZIP2_COMPRESSION=ON
BuildRequires:  bzip2-devel

%description
A free package dependency solver using a satisfiability algorithm. The
library is based on two major, but independent, blocks:

- Using a dictionary approach to store and retrieve package
  and dependency information.

- Using satisfiability, a well known and researched topic, for
  resolving package dependencies.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       rpm-devel%{?_isa}

%description devel
Development files for %{name}.

%package tools
Summary:        Package dependency solver tools
Requires:       %{name}%{?_isa} = %{version}-%{release}
# repo2solv dependencies. All of those are used in shell-script.
Requires:       %{_bindir}/gzip
Requires:       %{_bindir}/bzip2
Requires:       %{_bindir}/lzma
Requires:       %{_bindir}/xz
Requires:       %{_bindir}/cat
Requires:       %{_bindir}/find

%description tools
Package dependency solver tools.

%package demo
Summary:        Applications demoing the %{name} library
Requires:       %{name}%{?_isa} = %{version}-%{release}
# solv dependencies. Used as execlp() and system()
Requires:       %{_bindir}/curl
Requires:       %{_bindir}/gpg2

%description demo
Applications demoing the %{name} library.

%if %{with perl_bindings}
%package -n perl-%{libname}
Summary:        Perl bindings for the %{name} library
BuildRequires:  swig
BuildRequires:  perl-devel
BuildRequires:  perl-generators
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n perl-%{libname}
Perl bindings for the %{name} library.
%endif

%if %{with ruby_bindings}
%package -n ruby-%{libname}
Summary:        Ruby bindings for the %{name} library
BuildRequires:  swig
BuildRequires:  ruby-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n ruby-%{libname}
Ruby bindings for the %{name} library.
%endif

%if %{with python_bindings}
%package -n python2-%{libname}
Summary:        Python bindings for the %{name} library
%{?python_provide:%python_provide python2-%{libname}}
BuildRequires:  swig
BuildRequires:  python2-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python2-%{libname}
Python bindings for the %{name} library.

Python 2 version.

%if %{with python3}
%package -n python3-%{libname}
Summary:        Python bindings for the %{name} library
%{?python_provide:%python_provide python3-%{libname}}
BuildRequires:  swig
BuildRequires:  python3-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{libname}
Python bindings for the %{name} library.

Python 3 version.
%endif
%endif

%prep
# XXX: switch to %{?commit:-n %{name}-%{commit}} in RPM 4.14
%autosetup -p1 -n %{name}-%{commit}
mkdir build

%build
pushd build
  %cmake                                          \
    -DFEDORA=1                                    \
    -DENABLE_RPMDB=ON                             \
    -DENABLE_RPMDB_BYRPMHEADER=ON                 \
    -DENABLE_RPMMD=ON                             \
    %{?with_comps:-DENABLE_COMPS=ON}              \
    %{?with_appdata:-DENABLE_APPDATA=ON}          \
    -DUSE_VENDORDIRS=ON                           \
    -DWITH_LIBXML2=ON                             \
    -DENABLE_LZMA_COMPRESSION=ON                  \
    -DENABLE_BZIP2_COMPRESSION=ON                 \
    %{?with_helix_repo:-DENABLE_HELIXREPO=ON}     \
    %{?with_suse_repo:-DENABLE_SUSEREPO=ON}       \
    %{?with_debian_repo:-DENABLE_DEBIAN=ON}       \
    %{?with_arch_repo:-DENABLE_ARCHREPO=ON}       \
    %{?with_multi_semantics:-DMULTI_SEMANTICS=ON} \
    %{?with_complex_deps:-DENABLE_COMPLEX_DEPS=1} \
    %{?with_perl_bindings:-DENABLE_PERL=ON}       \
    %{?with_ruby_bindings:-DENABLE_RUBY=ON}       \
%if %{with python_bindings}
    -DENABLE_PYTHON=ON                            \
%if %{with python3}
    -DENABLE_PYTHON3=ON                           \
    -DPYTHON3_EXECUTABLE=%{__python3}             \
%endif
%endif
    ..
  %make_build
popd

%install
pushd build
  %make_install
popd

mv %{buildroot}%{_bindir}/repo2solv.sh %{buildroot}%{_bindir}/repo2solv

%check
pushd build
  ctest -VV
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE*
%doc README
%{_libdir}/%{name}.so.*
%{_libdir}/%{name}ext.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/%{name}ext.so
%{_includedir}/%{libname}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}ext.pc
# Own directory because we don't want to depend on cmake
%dir %{_datadir}/cmake/Modules/
%{_datadir}/cmake/Modules/FindLibSolv.cmake
%{_mandir}/man3/%{name}*.3*

# Some small macro to list tools with mans
%global solv_tool() \
%{_bindir}/%{1}\
%{_mandir}/man1/%{1}.1*

%files tools
%solv_tool deltainfoxml2solv
%solv_tool dumpsolv
%solv_tool installcheck
%solv_tool mergesolv
%solv_tool repomdxml2solv
%solv_tool rpmdb2solv
%solv_tool rpmmd2solv
%solv_tool rpms2solv
%solv_tool testsolv
%solv_tool updateinfoxml2solv
%if %{with comps}
  %solv_tool comps2solv
%endif
%if %{with appdata}
  %solv_tool appdata2solv
%endif
%if %{with debian_repo}
  %solv_tool deb2solv
%endif
%if %{with arch_repo}
  %solv_tool archpkgs2solv
  %solv_tool archrepo2solv
%endif
%if %{with helix_repo}
  %solv_tool helix2solv
%endif
%if %{with suse_repo}
  %solv_tool susetags2solv
%endif

%{_bindir}/repo2solv

%files demo
%{_bindir}/solv

%if %{with perl_bindings}
%files -n perl-%{libname}
%{perl_vendorarch}/%{libname}.pm
%{perl_vendorarch}/%{libname}.so
%endif

%if %{with ruby_bindings}
%files -n ruby-%{libname}
%{ruby_vendorarchdir}/%{libname}.so
%endif

%if %{with python_bindings}
%files -n python2-%{libname}
%{python2_sitearch}/_%{libname}.so
%{python2_sitearch}/%{libname}.py*

%if %{with python3}
%files -n python3-%{libname}
%{python3_sitearch}/_%{libname}.so
%{python3_sitearch}/%{libname}.py
%{python3_sitearch}/__pycache__/%{libname}.*
%endif
%endif

%changelog
* Mon Mar 27 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.6.26-5.git.20.668e249
- Update to latest snapshot

* Sat Mar 18 2017 Neal Gompa <ngompa13@gmail.com> - 0.6.26-4.git.19.2262346
- Enable AppData support (#1427171)

* Thu Mar 16 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.26-3.git.19.2262346
- Update to latest git
- Switch to libxml2

* Mon Mar 06 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.26-2
- Use %%{__python3} as PYTHON3_EXECUTABLE

* Wed Feb 15 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.26-1
- Update to 0.6.26

* Tue Feb 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.25-1
- Update to 0.6.25

* Fri Jan 13 2017 Vít Ondruch <vondruch@redhat.com> - 0.6.24-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.6.24-3
- Rebuild for Python 3.6

* Fri Dec 09 2016 Orion Poplawski <orion@cora.nwra.com> - 0.6.24-2
- Use upstream python build options

* Fri Nov 11 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.24-1
- Update to 0.6.24

* Sat Oct 29 2016 Denis Ollier <larchunix@gmail.com> - 0.6.23-6
- Typo fixes in spec: s/MULTI_SYMANTICS/MULTI_SEMANTICS/

* Tue Sep 13 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.23-5
- Trivial fixes in spec

* Sat Aug 27 2016 Neal Gompa <ngompa13@gmail.com> - 0.6.23-4
- Enable suserepo on Fedora to enable making openSUSE containers with Zypper

* Fri Aug 12 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.23-3
- Enable helixrepo on Fedora

* Wed Aug 03 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.23-2
- Backport patch to fix dnf --debugsolver crash (RHBZ #1361831)

* Wed Jul 27 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.23-1
- Update to 0.6.23

* Wed Jul 20 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.22-3
- Backport couple of patches from upstream

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.22-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.22-1
- Update to 0.6.22
- Backport patch which will help to not autoremove needed packages
  (RHBZ #1227066, #1284349)

* Mon Jun 06 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.21-3
- Enable deb/arch support for non-rhel distros

* Mon May 30 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.21-2
- Modify enabled/disabled features

* Wed May 18 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.21-1
- Update to 0.6.21

* Tue May 17 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.20-2
- Backport patch to fix crashing on reading some repos (RHBZ #1318662)
- Backport patch to fix installing multilib packages with weak deps
  (RHBZ #1325471)

* Sat Apr 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.20-1
- Update to 0.6.20

* Tue Apr 05 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.19-3
- Reorganize spec file
- Enable helixrepo feature
- enable appdata feature

* Tue Mar 8 2016 Jaroslav Mracek <jmracek@redhat.com> - 0.6.19-2
- Apply 9 patches from upstream

* Sat Feb 27 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.19-1
- Update to 0.6.19

* Tue Feb  2 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.15-6
- Explicitly add rubypick and ruubygems build dependencies

* Tue Jan 12 2016 Vít Ondruch <vondruch@redhat.com> - 0.6.15-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Sun Jan 10 2016 Dan Horák <dan[at]danny.cz> - 0.6.15-4
- fix build on non-Fedora with python3

* Tue Jan 05 2016 Jaroslav Mracek <jmracek@redhat.com> - 0.6.15-3
- Fix bz2 compression support for python3 (RhBug:1293652)

* Fri Dec 18 2015 Michal Luscon <mluscon@redhat.com> - 0.6.15-2
- Revert reworked multiversion orphaned handling

* Thu Dec 17 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.15-1
- Update to 0.6.15

* Tue Dec 08 2015 Jaroslav Mracek <jmracek@redhat.com> - 0.6.14-7
- Rebase to upstream b1ea392
- Enable bz2 compression support (Mikolaj Izdebski <mizdebsk@redhat.com>) (RhBug:1226647)

* Thu Nov 26 2015 Adam Williamson <awilliam@redhat.com> - 0.6.14-6
- revert obsolete, as %%python_provide does it (undocumented)

* Wed Nov 18 2015 Adam Williamson <awilliam@redhat.com> - 0.6.14-5
- adjust obsolete for stupid packaging

* Wed Nov 18 2015 Adam Williamson <awilliam@redhat.com> - 0.6.14-4
- python2-solv obsoletes python-solv (#1263230)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.14-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 14 2015 Michal Luscon <mluscon@redhat.com> - 0.6.14-2
- Backport patches from upstream

* Mon Oct 12 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.14-1
- Update to 0.6.14
- Backport patches from upstream

* Thu Sep 10 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.12-1
- Update to 0.6.12

* Wed Aug 05 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.11-3
- added compile flag to support rich dependencies
- new version adding MIPS support
- Distribute testsolv in -tools subpackage (Igor Gnatenko)
- Enable python3 bindings for fedora (Igor Gnatenko)

* Tue Aug 04 2015 Adam Williamson <awilliam@redhat.com> - 0.6.11-2
- make bindings require the exact matching version of the lib (#1243737)

* Mon Jun 22 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.11-1
- new version fixing segfault
- RbConfig fixed in the upstream (1928f1a), libsolv-ruby22-rbconfig.patch erased

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.10-1
- new version fixing segfault

* Fri Mar 6 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.8-3
- Rebuilt with new provides selection feature

* Mon Jan 19 2015 Vít Ondruch <vondruch@redhat.com> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Fri Jan 16 2015 Richard Hughes <richard@hughsie.com> - 0.6.8-2
- Update to latest upstream release to fix a crash in PackageKit.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild


* Mon Aug 11 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.4-2
- Rebase to upstream 12af31a

* Mon Jul 28 2014 Aleš Kozumplík <akozumpl@redhat.com> - 0.6.4-1
- Rebase to upstream 5bd9589

* Mon Jul 14 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.4-0.git2a5c1c4
- Rebase to upstream 2a5c1c4
- Filename selector can start with a star

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2.git6d968f1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Aleš Kozumplík <ales@redhat.com> - 0.6.1-1.git6d968f1
- Rebase to upstream 6d968f1
- Fix RhBug:1049209

* Fri Apr 25 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.1-0.gitf78f5de
- Rebase to 0.6.0, upstream commit f78f5de.

* Thu Apr 24 2014 Vít Ondruch <vondruch@redhat.com> - 0.6.0-0.git05baf54.1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Wed Apr 9 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.0-0.git05baf54
- Rebase to 0.6.0, upstream commit 05baf54.

* Mon Dec 16 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.4.1-1.gitbcedc98
- Rebase upstream bcedc98
- Fix RhBug:1051917.

* Mon Dec 16 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.4.1-0.gita8e47f1
- Rebase to 0.4.1, upstream commit a8e47f1.

* Fri Nov 22 2013 Zdenek Pavlas <zpavlas@redhat.com> - 0.4.0-2.git4442b7f
- Rebase to 0.4.0, upstream commit 4442b7f.
- support DELTA_LOCATION_BASE for completeness

* Tue Oct 29 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.4.0-1.gitd49d319
- Rebase to 0.4.0, upstream commit d49d319.

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.3.0-9.gita59d11d
- Perl 5.18 rebuild

* Wed Jul 31 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-8.gita59d11d
- Rebase to upstream a59d11d.

* Fri Jul 19 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-7.git228d412
- Add build flags, including Deb, Arch, LZMA and MULTI_SEMANTICS. (RhBug:985905)

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.3.0-6.git228d412
- Perl 5.18 rebuild

* Mon Jun 24 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-5.git228d412
- Rebase to upstream 228d412.
- Fixes hawkey github issue https://github.com/akozumpl/hawkey/issues/13

* Thu Jun 20 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-4.git209e9cb
- Rebase to upstream 209e9cb.
- Package the new man pages.

* Thu May 16 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-3.git7399ad1
- Run 'make test' with libsolv build.

* Mon Apr 8 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-2.git7399ad1
- Rebase to upstream 7399ad1.
- Fixes RhBug:905209

* Mon Apr 8 2013 Aleš Kozumplík <akozumpl@redhat.com> - 0.3.0-1.gite372b78
- Rebase to upstream e372b78.
- Fixes RhBug:e372b78

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-2.gitf663ca2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 23 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-17.git6c9d3eb
- Rebase to upstream 6c9d3eb.
- Drop the solv.i stdbool.h fix integrated upstream.
- Dropped the job reasons fix.

* Mon Jul 23 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-16.git1617994
- Fix build problems with Perl bindings.

* Mon Jul 23 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-15.git1617994
- Rebuilt after a failed mass rebuild.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.0-14.git1617994
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Aleš Kozumplik <akozumpl@redhat.com> - 0.0.0-13.git1617994%{?dist}
- preliminary fix for JOB resons in solver_describe_decision().

* Sun Jul 1 2012 Aleš Kozumplik <akozumpl@redhat.com> - 0.0.0-12.git1617994%{?dist}
- Rebase to upstream 1617994.
- Support for RPM_ADD_WITH_HDRID.

* Thu Jun  7 2012 Aleš Kozumplik <akozumpl@redhat.com> - 0.0.0-11.gitd39a42b%{?dist}
- Rebase to upstream d39a42b.
- Fix the epochs.
- Move the ruby modules into vendorarch dir, where they are expected.

* Thu May  17 2012 Aleš Kozumplik <akozumpl@redhat.com> - 0.0.0-9.git8cf7650%{?dist}
- Rebase to upstream 8cf7650.
- ruby bindings: fix USE_VENDORDIRS for Fedora.

* Thu Apr  12 2012 Aleš Kozumplik <akozumpl@redhat.com> - 0.0.0-7.gitaf1465a2%{?dist}
- Rebase to the upstream.
- Make repo_add_solv() work without stub repodata.

* Thu Apr  5 2012 Karel Klíč <kklic@redhat.com> - 0.0.0-6.git80afaf7%{?dist}
- Rebuild for the new libdb package.

* Mon Apr  2 2012 Karel Klíč <kklic@redhat.com> - 0.0.0-5.git80afaf7%{?dist}
- Rebuild for the new rpm package.

* Wed Mar 21 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-4.git80afaf7%{?dist}
- New upstream version, fix the .rpm release number.

* Wed Mar 21 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-3.git80afaf7%{?dist}
- New upstream version.

* Tue Feb  7 2012 Karel Klíč <kklic@redhat.com> - 0.0.0-2.git857fe28%{?dist}
- Adapted to Ruby 1.9.3 (workaround for broken CMake in Fedora and
  ruby template correction in bindings)

* Thu Feb  2 2012 Karel Klíč <kklic@redhat.com> - 0.0.0-1.git857fe28
- Initial packaging
- Based on Jindra Novy's spec file
- Based on upstream spec file
