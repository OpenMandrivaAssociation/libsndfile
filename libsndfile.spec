%define	major	1
%define	libname	%mklibname sndfile %{major}
%define	devname	%mklibname sndfile -d

%bcond_with	octave
%bcond_with	bootstrap

Summary:	A library to handle various audio file formats
Name:		libsndfile
Version:	1.0.25
Release:	5
License:	LGPLv2+
Group:		Sound
URL:		http://www.mega-nerd.com/libsndfile/
Source0:	http://www.mega-nerd.com/libsndfile/files/%{name}-%{version}.tar.gz
Patch0:		libsndfile-1.0.25-support-newer-octave-versions.patch

BuildRequires:	autogen
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(celt)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(vorbis)
%if !%{with bootstrap}
%ifarch %{ix86} x86_64
BuildRequires:	nasm
%endif
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(samplerate)
%endif

%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

%package -n	%{libname}
Summary:	Shared library of sndfile
Group:		System/Libraries

%description -n	%{libname}
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

This package contains the shared library to run applications based on
libsndfile.

%package -n	%{devname}
Summary:	Libraries, includes, etc to develop libsndfile applications 
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	sndfile-devel = %{version}-%{release}

%description -n	%{devname}
Libraries, include files, etc you can use to develop libsndfile applications.

%package	progs
Summary:	Example progs based on libsndfile
Group:		Sound 

%description	progs
This contains sndfile-info for printing information about a sound
file and sndfile-play for playing a sound file.

%if %{with octave}
%package	octave
Summary:	Octave modules based on libsndfile
Group:		Sound 
BuildRequires:	octave-devel

%description	octave
This contains octave modules based on libsndfile for reading, writing and 
playing audio files.
%endif

%prep
%setup -q
%patch0 -p1 -b .octave~
autoreconf -f -IM4

%build
%configure2_5x \
	--disable-static
%make

%install
%makeinstall_std 
rm -rf %{buildroot}%{_includedir}/FLAC

%multiarch_includes %{buildroot}%{_includedir}/sndfile.h

%files -n %{libname}
%doc AUTHORS NEWS README
%{_libdir}/libsndfile.so.%{major}*

%files -n %{devname}
%doc %{_docdir}/libsndfile1-dev
%doc ChangeLog 
%{_libdir}/libsndfile.so
%{multiarch_includedir}/sndfile.h
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_libdir}/pkgconfig/sndfile.pc

%files progs
%{_bindir}/sndfile-*
%{_mandir}/man1/*

%if %{with octave}
%files octave
%{_datadir}/octave/
%dir %{_libdir}/octave/*/site/oct/%{_target_platform}/sndfile
%{_libdir}/octave/*/site/oct/%{_target_platform}/sndfile/PKG_ADD
%{_libdir}/octave/*/site/oct/%{_target_platform}/sndfile/sndfile.oct
%endif



%changelog
* Fri Jun 01 2012 Andrey Bondrov <abondrov@mandriva.org> 1.0.25-4
+ Revision: 801782
- Bumb release and rebuild

* Sun Mar 11 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0.25-3
+ Revision: 784222
- seems like we don't build octave support by default..
- drop ancient obsoletes
- drop ancient obsoletes
- drop excessive dependencies
- fix octave build
- use pkgconfig() dependencies for buildrequires
- apply some cosmetics

* Tue Feb 07 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.25-2
+ Revision: 771615
- fix deps
- drop the static lib and the libtool *.la file
- various fixes

* Thu Jul 14 2011 Götz Waschk <waschk@mandriva.org> 1.0.25-1
+ Revision: 689974
- update to new version 1.0.25

* Mon Jun 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.24-3
+ Revision: 686316
- avoid pulling 32 bit libraries on 64 bit arch

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.24-2
+ Revision: 661680
- multiarch fixes

* Wed Mar 23 2011 Götz Waschk <waschk@mandriva.org> 1.0.24-1
+ Revision: 648117
- update to new version 1.0.24

* Sun Oct 10 2010 Götz Waschk <waschk@mandriva.org> 1.0.23-1mdv2011.0
+ Revision: 584532
- update to new version 1.0.23

* Mon Oct 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.22-1mdv2011.0
+ Revision: 582847
- 1.0.22

* Wed Dec 16 2009 Götz Waschk <waschk@mandriva.org> 1.0.21-2mdv2010.1
+ Revision: 479219
- rebuild, the src.rpm was lost
- new version
- fix source URL

* Wed Dec 02 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 1.0.20-6mdv2010.1
+ Revision: 472550
- Rebuild

* Wed Dec 02 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 1.0.20-5mdv2010.1
+ Revision: 472549
- Rebuild

* Sun Nov 08 2009 Götz Waschk <waschk@mandriva.org> 1.0.20-4mdv2010.1
+ Revision: 463218
- make devel packages parallely installable (bug #55361)

* Sun Sep 27 2009 Olivier Blin <blino@mandriva.org> 1.0.20-3mdv2010.0
+ Revision: 449995
- keep nasm for x86_64 too

* Sun Sep 27 2009 Olivier Blin <blino@mandriva.org> 1.0.20-2mdv2010.0
+ Revision: 449909
- add bootstrap flag for jack (from Arnaud Patard)
- use nasm on x86 only (from Arnaud Patard)

* Thu May 14 2009 Frederik Himpe <fhimpe@mandriva.org> 1.0.20-1mdv2010.0
+ Revision: 375705
- Update to new version 1.0.20

* Tue Mar 03 2009 Götz Waschk <waschk@mandriva.org> 1.0.19-1mdv2009.1
+ Revision: 347863
- update to new version 1.0.19

* Sat Feb 07 2009 Funda Wang <fwang@mandriva.org> 1.0.18-3mdv2009.1
+ Revision: 338398
- 1.0.18 final

* Tue Jan 13 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.18-2.pre25.1mdv2009.1
+ Revision: 328819
- update to new prerelease 25
- drop patch 0

* Mon Dec 08 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.18-2.pre24h.1mdv2009.1
+ Revision: 311954
- add missing buildrequires on libvorbis-devel, libsamplerate-devel and celt-devel
- update to new prerelease 24h

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.0.18-2.pre22.1mdv2009.0
+ Revision: 264893
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue May 27 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.18-1.pre22.1mdv2009.0
+ Revision: 211739
- update to new prerelease 1.0.18.pre22
- add missing buildrequires on nasm, libalsa-devel, libjack-devel and autogen
- Patch0: fix compilation with gcc-4.3
- do not package INSTALL file

* Thu Feb 21 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.18-1.pre20.1mdv2008.1
+ Revision: 173754
- new prerelease
- new license policy

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1.0.18-1.pre19.1mdv2008.1
+ Revision: 148600
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- do not package big ChangeLog

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Dec 07 2007 Götz Waschk <waschk@mandriva.org> 1.0.18-0.pre19.1mdv2008.1
+ Revision: 116243
- new version

* Mon Oct 22 2007 Götz Waschk <waschk@mandriva.org> 1.0.18-0.pre18.1mdv2008.1
+ Revision: 101137
- new version

* Wed Oct 10 2007 Götz Waschk <waschk@mandriva.org> 1.0.18-0.pre17.1mdv2008.1
+ Revision: 96686
- new prerelease
- drop the patch
- add support for octave, but disable it by default

* Mon Oct 01 2007 Götz Waschk <waschk@mandriva.org> 1.0.18-0.pre11.7mdv2008.0
+ Revision: 94331
- fix oden's fix
- security update (bug #34388, CVE-2007-4974)

  + Oden Eriksson <oeriksson@mandriva.com>
    - fix CVE-2007-4974

* Wed Jun 27 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.18-0.pre11.6mdv2008.0
+ Revision: 44810
- add more provides

* Sun Jun 24 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.18-0.pre11.5mdv2008.0
+ Revision: 43667
- adjust obsoletes

* Sat Jun 23 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.18-0.pre11.4mdv2008.0
+ Revision: 43482
- new devel library policy

* Thu Jun 14 2007 Helio Chissini de Castro <helio@mandriva.com> 1.0.18-0.pre11.3mdv2008.0
+ Revision: 39359
- Add flac requires. If you intend to compile with flac resources, prefer external library instead of internal one, conflicting with libflac-devel on includes install

* Thu Jun 14 2007 Götz Waschk <waschk@mandriva.org> 1.0.18-0.pre11.2mdv2008.0
+ Revision: 39316
- remove conflicting flac headers

* Wed Jun 13 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.18-0.pre11.1mdv2008.0
+ Revision: 38952
- prerelease 11
- fix file list
- spec file clean

* Tue May 01 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.18-0.pre8.1mdv2008.0
+ Revision: 20133
- update to the 1.0.18pre8 version
- drop P0
- drop auto* aclocal actions


* Mon Dec 11 2006 Götz Waschk <waschk@mandriva.org> 1.0.17-5mdv2007.0
+ Revision: 94980
- fix buildrequires
- fix buildrequires
- fix buildrequires
- Import libsndfile

* Mon Dec 11 2006 G�tz Waschk <waschk@mandriva.org> 1.0.17-3mdv2007.1
- patch for new libflac

* Mon Sep 04 2006 Emmanuel Andry <eandry@mandriva.org> 1.0.17-2mdv2007.0
- add provides for static package

* Fri Sep 01 2006 G�tz Waschk <waschk@mandriva.org> 1.0.17-1mdv2007.0
- update file list
- New release 1.0.17

* Mon May 01 2006 Götz Waschk <waschk@mandriva.org> 1.0.16-1mdk
- New release 1.0.16

* Fri Mar 17 2006 Götz Waschk <waschk@mandriva.org> 1.0.15-1mdk
- New release 1.0.15

* Tue Feb 21 2006 Götz Waschk <waschk@mandriva.org> 1.0.14-1mdk
- New release 1.0.14

* Mon Jan 23 2006 Götz Waschk <waschk@mandriva.org> 1.0.13-1mdk
- New release 1.0.13
- use mkrel

* Wed Oct 05 2005 G�tz Waschk <waschk@mandriva.org> 1.0.12-1mdk
- fix buildrequires
- New release 1.0.12

* Mon Nov 15 2004 Goetz Waschk <waschk@linux-mandrake.com> 1.0.11-1mdk
- New release 1.0.11

* Thu Jun 17 2004 G�tz Waschk <waschk@linux-mandrake.com> 1.0.10-1mdk
- fix url
- reenable libtoolize
- New release 1.0.10

* Fri Apr 02 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.0.9-1mdk
- 1.0.9
- fix libtoolize

