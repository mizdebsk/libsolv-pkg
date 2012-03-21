%global gitrev 80afaf7
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}
%filter_provides_in %{perl_vendorarch}/.*\.so$
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_provides_in %{ruby_sitearch}/.*\.so$
%filter_setup

Name:		libsolv
Version:	0.0.0
Release:	4.git%{gitrev}%{?dist}
License:	BSD
Url:		https://github.com/openSUSE/libsolv
# git clone https://github.com/openSUSE/libsolv.git
# git archive %{gitrev} --prefix=libsolv/ | xz > libsolv-%{gitrev}.tar.xz
Source:		libsolv-%{gitrev}.tar.xz
Patch0:		libsolv-rubyinclude.patch
Patch1:		libsolv-newruby.patch
Group:		Development/Libraries
Summary:	Package dependency solver
BuildRequires:	cmake libdb-devel expat-devel rpm-devel zlib-devel
BuildRequires:	swig perl perl-devel ruby ruby-devel python2-devel
%description
A free package dependency solver using a satisfiability algorithm. The
library is based on two major, but independent, blocks:

- Using a dictionary approach to store and retrieve package
  and dependency information.

- Using satisfiability, a well known and researched topic, for
  resolving package dependencies.

%package devel
Summary:	A new approach to package dependency solving
Group:		Development/Libraries
Requires:	libsolv-tools%{?_isa} = %version
Requires:	libsolv%{?_isa} = %version
Requires:	rpm-devel%{?_isa}
Requires:	cmake

%description devel
Development files for libsolv,

%package tools
Summary:	A new approach to package dependency solving
Group:		Development/Libraries
Requires:	gzip bzip2 coreutils

%description tools
Package dependency solver tools.

%package demo
Summary:	Applications demoing the libsolv library
Group:		Development/Libraries
Requires:	curl gnupg2

%description demo
Applications demoing the libsolv library.

%package -n ruby-solv
Summary:	Ruby bindings for the libsolv library
Group:		Development/Languages

%description -n ruby-solv
Ruby bindings for sat solver.

%package -n python-solv
Summary:	Python bindings for the libsolv library
Group:		Development/Languages
Requires:	python

%description -n python-solv
Python bindings for sat solver.

%package -n perl-solv
Summary:	Perl bindings for the libsolv library
Group:		Development/Languages
Requires:	perl

%description -n perl-solv
Perl bindings for sat solver.

%prep
%setup -q -n libsolv
%patch0 -p1 -b .rubyinclude
%patch1 -p1 -b .newruby

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DENABLE_PERL=1 \
       -DENABLE_PYTHON=1 \
       -DENABLE_RUBY=1 \
       -DUSE_VENDORDIRS=1 \
       -DFEDORA=1

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT/usr/bin/testsolv

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE* README BUGS
%_libdir/libsolv.so.*
%_libdir/libsolvext.so.*

%files tools
%_bindir/deltainfoxml2solv
%_bindir/dumpsolv
%_bindir/installcheck
%_bindir/mergesolv
%_bindir/repo2solv.sh
%_bindir/repomdxml2solv
%_bindir/rpmdb2solv
%_bindir/rpmmd2solv
%_bindir/rpms2solv
%_bindir/updateinfoxml2solv

%files devel
%doc examples/solv.c
%_libdir/libsolv.so
%_libdir/libsolvext.so
%_includedir/solv
%_datadir/cmake/Modules/FindLibSolv.cmake

%files demo
%_bindir/solv

%files -n perl-solv
%doc examples/p5solv
%{perl_vendorarch}/*

%files -n ruby-solv
%doc examples/rbsolv
%{ruby_sitearch}/*

%files -n python-solv
%doc examples/pysolv
%{python_sitearch}/*

%changelog
* Wed Mar 21 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-4.git%{gitrev}%{?dist}
- New upstream version, fix the .rpm release number.

* Wed Mar 21 2012 Aleš Kozumplík <akozumpl@redhat.com> - 0.0.0-3.git%{gitrev}%{?dist}
- New upstream version.

* Tue Feb  7 2012 Karel Klíč <kklic@redhat.com> - 0.0.0-2.git857fe28%{?dist}
- Adapted to Ruby 1.9.3 (workaround for broken CMake in Fedora and
  ruby template correction in bindings)

* Thu Feb  2 2012 Karel Klíč <kklic@redhat.com> - 0.0.0-1.git857fe28
- Initial packaging
- Based on Jindra Novy's spec file
- Based on upstream spec file
