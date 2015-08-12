## Git
- git-plus > 5.1

安装时候可能会遇到 500， atom gyp ERR! stack Error: 500 status code downloading tarball
据说是302跳转没有follow，根据这个issue，设置环境变量
`export ATOM_NODE_URL=http://gh-contractor-zcbenz.s3.amazonaws.com/atom-shell/dist`
reference: https://github.com/atom/apm/issues/322
