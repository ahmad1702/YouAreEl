const clipBoard = (codename) => {
  /* Get the text field */
  var copyText = document.getElementById("finalcodename");


  let codenames = String(copyText.innerText);

  let url = "127.0.0.1:5000/" + codenames;
  console.log(url);

  const cb = navigator.clipboard;
  cb.writeText(url)

//   setTimeout(
//     async () => console.log(await window.navigator.clipboard.writeText(url)),
//     100
//   );

//   /* Alert the copied text */
//   alert("Copied the text: " + copyText.innerText);
};
