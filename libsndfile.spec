%define	major	1
%define	libname	%mklibname sndfile %{major}
%define	devname	%mklibname sndfile -d
%define	static	%mklibname sndfile -d -s

%bcond_without	octave
%bcond_with	bootstrap

Summary:	A library to handle various audio file formats
Name:		libsndfile
Version:	1.0.25
Release:	2
License:	LGPLv2+
Group:		Sound
URL:		http://www.mega-nerd.com/libsndfile/
Source0:	http://www.mega-nerd.com/libsndfile/files/%{name}-%{version}.tar.gz
Patch0:		libsndfile-1.0.25-support-newer-octave-versions.patch
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(alsa)
%if !%{with bootstrap}
%ifarch %{ix86} x86_64
BuildRequires:	nasm
%endif
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(samplerate)
%endif
BuildRequires:	pkgconfig(celt)
BuildRequires:	autogen

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
%configure2_5x
%make

%install
%makeinstall_std 
rm -rf %{buildroot}%{_includedir}/FLAC

%multiarch_includes %{buildroot}%{_includedir}/sndfile.h

rm -f %{buildroot}%{_libdir}/*.*a

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
