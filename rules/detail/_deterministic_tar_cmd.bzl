def deterministic_tar_cmd(tarball, folder):
    return """
tar --sort=name \
    --mtime="2015-01-01 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -cf {tarball} -C {folder} .""".format(tarball = tarball, folder = folder)