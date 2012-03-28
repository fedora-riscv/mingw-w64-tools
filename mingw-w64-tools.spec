%global snapshot_date 20120124

Name:           mingw-w64-tools
Version:        2.0.999
Release:        0.3.trunk.%{snapshot_date}%{?dist}
Summary:        Supplementary tools which are part of the mingw-w64 toolchain

License:        Public Domain
Group:          Development/Libraries
URL:            http://mingw-w64.sourceforge.net/
%if 0%{?snapshot_date}
Source0:        http://sourceforge.net/projects/mingw-w64/files/Toolchain%20sources/Automated%20Builds/mingw-w64-src_%{snapshot_date}.tar.bz2
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
%setup -q -D -T -n mingw-w64-v%{version}/mingw
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
        %configure
        make %{?_smp_mflags}
    popd
popd


%install
pushd mingw-w64-tools
    make -C gendef DESTDIR=$RPM_BUILD_ROOT install
    make -C genidl DESTDIR=$RPM_BUILD_ROOT install
    make -C widl DESTDIR=$RPM_BUILD_ROOT install
popd


%files
%doc COPYING
%{_bindir}/gendef
%{_bindir}/genidl
%{_bindir}/mingw-w64-widl


%changelog
* Wed Mar 28 2012 Dan Horák <dan[at]danny.cz> - 2.0.999-0.3.trunk.20120124
- fix build on s390(x)

* Sun Mar 11 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.2.trunk.20120124
- Eliminated several conditionals

* Mon Jan 30 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.1.trunk.20120124
- Initial package

