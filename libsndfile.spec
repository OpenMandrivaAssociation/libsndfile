# mpg123 uses libsndfile, wine uses mpg123
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 1
%define libname %mklibname sndfile
%define oldlibname %mklibname sndfile 1
%define devname %mklibname sndfile -d
%define lib32name %mklib32name sndfile %{major}
%define dev32name %mklib32name sndfile -d

%bcond_with	octave
%bcond_with	bootstrap

Summary:	A library to handle various audio file formats
Name:		libsndfile
Version:	1.2.2
Release:	2
License:	LGPLv2+
Group:		Sound
Url:		https://www.mega-nerd.com/libsndfile/
# https://github.com/erikd/libsndfile
Source0:	https://github.com/libsndfile/libsndfile/releases/download/%{version}/libsndfile-%{version}.tar.xz
Patch0:	libsndfile-1.0.25-system-gsm.patch
BuildRequires:	gsm-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(celt)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(opus)
%if !%{with bootstrap}
%ifarch %{ix86} %{x86_64}
BuildRequires:	nasm
%endif
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(samplerate)
%endif
%if %{with compat32}
BuildRequires:	devel(libasound)
BuildRequires:	devel(libogg)
BuildRequires:	devel(libvorbis)
BuildRequires:	devel(libgsm)
BuildRequires:	libc6
%endif

%description
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

%package -n	%{libname}
Summary:	Shared library of sndfile
Group:		System/Libraries
# (tpg) add compat provides
%rename %{oldlibname}
%if "%_lib" == "lib64"
Provides:		libsndfile.so.1(libsndfile.so.1.0)(64bit)
%else
Provides:		libsndfile.so.1(libsndfile.so.1.0)
%endif

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

%if %{with compat32}
%package -n	%{lib32name}
Summary:	Shared library of sndfile (32-bit)
Group:		System/Libraries
Provides:	libsndfile.so.1(libsndfile.so.1.0)
Requires:	libc6

%description -n	%{lib32name}
libsndfile is a C library for reading and writing sound files such as
AIFF, AU and WAV files through one standard interface. It can currently
read/write 8, 16, 24 and 32-bit PCM files as well as 32-bit floating
point WAV files and a number of compressed formats.

This package contains the shared library to run applications based on
libsndfile.

%package -n	%{dev32name}
Summary:	Libraries, includes, etc to develop libsndfile applications  (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n	%{dev32name}
Libraries, include files, etc you can use to develop libsndfile applications.
%endif

%prep
%autosetup -p1

rm -r src/GSM610
autoreconf -fi -IM4

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32
cd ..
%endif

mkdir build
cd build
%configure

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build
rm -rf %{buildroot}%{_includedir}/FLAC

%files -n %{libname}
%{_libdir}/libsndfile.so.%{major}*

%files -n %{devname}
%doc AUTHORS README
%doc %{_docdir}/libsndfile
%doc ChangeLog
%{_libdir}/libsndfile.so
%{_includedir}/sndfile.h
%{_includedir}/sndfile.hh
%{_libdir}/pkgconfig/sndfile.pc

%files progs
%{_bindir}/sndfile-*
%doc %{_mandir}/man1/*

%if %{with octave}
%files octave
%{_datadir}/octave/
%dir %{_libdir}/octave/*/site/oct/%{_target_platform}/sndfile
%{_libdir}/octave/*/site/oct/%{_target_platform}/sndfile/PKG_ADD
%{_libdir}/octave/*/site/oct/%{_target_platform}/sndfile/sndfile.oct
%endif

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libsndfile.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libsndfile.so
%{_prefix}/lib/pkgconfig/sndfile.pc
%endif
