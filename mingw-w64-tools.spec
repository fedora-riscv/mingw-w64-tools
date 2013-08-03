%global snapshot_date 20130403
%global branch trunk

Name:           mingw-w64-tools
Version:        2.0.999
Release:        0.8.%{branch}.%{snapshot_date}%{?dist}
Summary:        Supplementary tools which are part of the mingw-w64 toolchain

# http://sourceforge.net/mailarchive/forum.php?thread_name=5157C0FC.1010309%40users.sourceforge.net&forum_name=mingw-w64-public
# The tools gendef and genidl are GPLv3+, widl is LGPLv2+
License:        GPLv3+ and LGPLv2+

Group:          Development/Libraries
URL:            http://mingw-w64.sourceforge.net/
%if 0%{?snapshot_date}
# To regerenate a snapshot:
# wget http://mingw-w64.svn.sourceforge.net/viewvc/mingw-w64/%{branch}/?view=tar -O mingw-w64-%{branch}-snapshot-$(date '+%Y%m%d').tar.gz
Source0:        mingw-w64-%{branch}-snapshot-%{snapshot_date}.tar.gz
%else
Source0:        http://downloads.sourceforge.net/project/mingw-w64/mingw-w64/mingw-w64-release/mingw-w64-v%{version}.tar.gz
%endif
# just to make widl to build on s390
Patch0:         %{name}-2.0.999-s390.patch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95


%description
Supplementary tools which are part of the mingw-w64 toolchain
It contains gendef, genidl and mingw-w64-widl


%prep
%if 0%{?snapshot_date}
rm -rf mingw-w64-v%{version}
mkdir mingw-w64-v%{version}
cd mingw-w64-v%{version}
tar -xf %{S:0}
%setup -q -D -T -n mingw-w64-v%{version}/%{branch}
%else
%setup -q -n mingw-w64-v%{version}
%endif
%patch0 -p2 -b .s390


%build
pushd mingw-w64-tools
    pushd gendef
        %configure
        make %{?_smp_mflags}
    popd

    pushd genidl
        %configure
        make %{?_smp_mflags}
    popd

    pushd widl
        # widl needs to be aware of the location of the IDL files belonging
        # to the toolchain. Therefore it needs to be built for both the win32
        # and win64 targets
        %global _configure ../configure
        mkdir win32
        pushd win32
          %configure --target=%{mingw32_target} --program-prefix=%{mingw32_target}-
          make %{?_smp_mflags}
        popd
        mkdir win64
        pushd win64
          %configure --target=%{mingw64_target} --program-prefix=%{mingw64_target}-
          make %{?_smp_mflags}
        popd
    popd
popd


%install
pushd mingw-w64-tools
    make -C gendef DESTDIR=$RPM_BUILD_ROOT install
    make -C genidl DESTDIR=$RPM_BUILD_ROOT install
    make -C widl/win32 DESTDIR=$RPM_BUILD_ROOT install
    make -C widl/win64 DESTDIR=$RPM_BUILD_ROOT install
popd


%files
%doc COPYING
%{_bindir}/gendef
%{_bindir}/genidl
%{_bindir}/%{mingw32_target}-widl
%{_bindir}/%{mingw64_target}-widl


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.999-0.8.trunk.20130403
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.7.trunk.20130403
- Update to 20130403 snapshot
- Use a different source tarball which doesn't contain unrelevant code (like libiberty)
- Removed Provides: bundled(libiberty)
- Make sure the widl tool is built for both win32 and win64 toolchains
- Upstream has changed the license of the gendef and genidl tools to GPLv3+
  The license of the widl tool is LGPLv2+

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.999-0.6.trunk.20120124
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Jon Ciesla <limburgher@gmail.com> - 2.0.999-0.5.trunk.20120124
- Provides: bundled(libiberty)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.999-0.4.trunk.20120124
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 28 2012 Dan Horák <dan[at]danny.cz> - 2.0.999-0.3.trunk.20120124
- fix build on s390(x)

* Sun Mar 11 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.2.trunk.20120124
- Eliminated several conditionals

* Mon Jan 30 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.1.trunk.20120124
- Initial package

