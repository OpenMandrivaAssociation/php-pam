%define modname pam
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A55_%{modname}.ini

Summary:	PAM integration for PHP
Name:		php-%{modname}
Version:	1.0.3
Release:	13
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
find -type f | xargs dos2unix

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


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-12mdv2012.0
+ Revision: 795484
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-11
+ Revision: 761276
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-10
+ Revision: 696453
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-9
+ Revision: 695448
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-8
+ Revision: 646669
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-7mdv2011.0
+ Revision: 629849
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-6mdv2011.0
+ Revision: 628170
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-5mdv2011.0
+ Revision: 600516
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-4mdv2011.0
+ Revision: 588854
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-3mdv2010.1
+ Revision: 514592
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-2mdv2010.1
+ Revision: 485414
- rebuilt for php-5.3.2RC1

* Wed Dec 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-1mdv2010.1
+ Revision: 475233
- 1.0.3

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-12mdv2010.1
+ Revision: 468207
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-11mdv2010.0
+ Revision: 451316
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1.0.2-10mdv2010.0
+ Revision: 397562
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-9mdv2010.0
+ Revision: 377011
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-8mdv2009.1
+ Revision: 346525
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-7mdv2009.1
+ Revision: 341783
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-6mdv2009.1
+ Revision: 321885
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-5mdv2009.1
+ Revision: 310292
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-4mdv2009.0
+ Revision: 238417
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-3mdv2009.0
+ Revision: 200255
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdv2008.1
+ Revision: 162107
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Nov 28 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2008.1
+ Revision: 113772
- 1.0.2

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2mdv2008.1
+ Revision: 107703
- restart apache if needed

* Thu Sep 27 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1mdv2008.1
+ Revision: 93259
- 1.0.1

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-6mdv2008.0
+ Revision: 77565
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-5mdv2008.0
+ Revision: 39513
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-4mdv2008.0
+ Revision: 33867
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3mdv2008.0
+ Revision: 21347
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2007.0
+ Revision: 117604
- rebuilt against new upstream version (5.2.1)

* Mon Nov 13 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2007.0
+ Revision: 83617
- Import php-pam

* Mon Nov 13 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2007.1
- initial Mandriva package

