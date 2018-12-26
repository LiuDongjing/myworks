var objApp = window.external;
var objWindow = objApp.Window;
var objCommon = objApp.CreateWizObject("WizKMControls.WizCommonUI");
var objDatabase = objApp.Database;
var docs = objDatabase.GetAllDocuments();
var progress = objApp.CreateWizObject("WizKMControls.WizProgressWindow");
progress.Title = "Backup Wiz";
progress.Max = docs.Count;
progress.Show();
var docFailed = 0;
var attachFailed = 0;
var attachments = 0;
var downloaded = 0;
for (var i = 0; downloaded < 1 && i < docs.Count; i++) {
    var doc = docs.Item(i);
    progress.Text = doc.Title;
    if(!doc.Downloaded) {
        downloaded++;
        var flag = doc.CheckDocumentData(0);
        console.log("Flag: "+flag);
        console.log("DOC: "+doc.Title);
        if(!flag) {
            docFailed++;
            console.error("矛盾!");
            console.error("Document '" + doc.Title + "' download failed!");
        }
    }
    var atts = doc.Attachments;
    for (var j = 0; j < atts.Count; j++) {
        var att = atts.Item(j);
        attachments++;
        if(!att.CheckAttachmentData()) {
            attachFailed++;
            console.error("Attachment '" + att.Name + "' download failed!");
        }
    }
    progress.Pos = i + 1;
}

if (progress) {
    progress.Hide();
    progress.Destroy();
    progress = null;
}
objWindow.ShowMessage("共有"+docs.Count+"个文档，下载失败"+docFailed+"个。", "Wiz备份", 0x40);
objWindow.ShowMessage("共有"+attachments+"个附件，下载失败"+attachFailed+"个。", "Wiz备份", 0x40);