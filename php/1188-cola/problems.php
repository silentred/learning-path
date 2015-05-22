如果在popup框里使用editor的话，需要设定width和height, 否则都默认为0
<script type="text/javascript">
    var popEditor;
    popEditor = KindEditor.create('#plotContent', {
        width : '600px',
        height: '400px',
        allowFileManager: true,
        uploadJson: 'index.php?c=files&a=saveimgforeditor',
        fileManagerJson: 'index.php?c=files&a=filelistforedit',
        afterBlur: function () {
            this.sync();
        }
    });

</script>