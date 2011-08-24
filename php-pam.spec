%define modname pam
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A55_%{modname}.ini

Summary:	PAM integration for PHP
Name:		php-%{modname}
Version:	1.0.3
Release:	%mkrel 10
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/pam
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	pam-devel
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension provides PAM (Pluggable Authentication Modules) integration. PAM
is a system of libraries that handle the authentication tasks of applications
and services. The library provides a stable API for applications to defer to
for authentication tasks.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

# attribs fix
find -type f | xargs chmod 644

# crlf fix
find -type f | xargs dos2unix -U

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,/%{_lib}

%make
mv modules/*.so .

#%{_usrsrc}/php-devel/buildext %{modname} "pam.c" \
#    "-L/%{_lib}/security -L/%{_lib} -I%{_includedir}/security -lpam -ldl" \
#    "-DCOMPILE_DL_PAM -DHAVE_PAM -DHAVE_SECURITY_PAM_APPL_H"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}%{_libdir}/php/extensions

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[pam]
pam.servicename = "%{name}";
EOF

# fix conditional pam config file
%if %{mdkversion} < 200610
cat > %{buildroot}%{_sysconfdir}/pam.d/%{name} <<EOF
auth	sufficient	pam_pwdb.so shadow nodelay
account	sufficient	pam_pwdb.so
EOF
%else
cat > %{buildroot}%{_sysconfdir}/pam.d/%{name} <<EOF
#%PAM-1.0
auth	include	system-auth
account	include	system-auth
EOF
%endif

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README CREDITS package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
