(async () => {
  console.log("test1")
  data = ($('#my-data').data())
  nameData = data["name"]
  var testArray = nameData.split(",")
  testArray[0] = testArray[0].substring(1)
  testArray[testArray.length - 1] = testArray[testArray.length - 1].slice(0,-1)
  for (i = 0; i < testArray.length; i++) {
    var url = testArray[i]
    if (i == 0) {
    url = url.slice(1,-1)
    } else {
      url = url.slice(2,-1)
    }
    const loadingTask = PDFJS.getDocument(url);
    const pdf = await loadingTask.promise;
    const page = await pdf.getPage(1);
    var pdfName = "pdf" + String(i)
    const scale = 1;
    const viewport = page.getViewport(scale);
    const canvas = document.getElementById(pdfName);
  } 
})();
