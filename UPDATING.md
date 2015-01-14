How to update a package
=======================

This is a quick howto on updating packages and building them when new upstream
tarball is released.

It is assumed that you work on Fedora >= 20.

1. Make sure you have RPM development tools installed:

    yum install rpmdevtools mock rpm-build copr-cli

   and switch to the directory of the package you want to update.

2. Edit the package specfile to provide the new version (the `Version:` tag)
   and reset `Release:` to `0` (it should now say `0%{?dist}`).

3. To bump the `Release:` to `1` and create a new changelog entry, run.

    rpmdev-bumpspec -c "Update to <version>" <pkg>.spec

4. Get the new upstream tarball:

    wget -p --no-directories <PyPI-download-link>

5. Create a source RPM (`<pkg>-<version>-<release>.src.rpm`) by running:

    rpmbuild --define "_srcrpmdir ." --define "_sourcedir ." -bs <pkg>.spec

6. Optionally, you can now test the build in mock on different releases:

    # to test on RHEL/CentOS 6 or 7
    mock -v -r epel-6-x86_64 <pkg>-<version>-<release>.src.rpm
    mock -v -r epel-7-x86_64 <pkg>-<version>-<release>.src.rpm

    # to test on Fedora Rawhide or an active release, e.g. 21
    mock -v -r fedora-rawhide-x86_64 <pkg>-<version>-<release>.src.rpm
    mock -v -r fedora-21-x86_64 <pkg>-<version>-<release>.src.rpm

  If the build fails, fix it :)

7. Upload the source RPM somewhere public.

8. Start a new Copr build (assuming you have the rights to the Copr repo at
   https://copr.fedoraproject.org/coprs/pypa/pypa/). You can either do this
   in your browser at https://copr.fedoraproject.org/coprs/pypa/pypa/add_build/
   or from command line:

    copr build pypa/pypa <url-of-uploaded-source-rpm>

9. Watch the progress at the build page. If the build fails, fix the specfile,
   run `rpmdev-bumpspec -c "Fixed what went wrong"` and go to step 6.

10. If the build succeeds, be happy and don't forget to commit the changes.
