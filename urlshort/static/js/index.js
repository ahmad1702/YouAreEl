const clipBoard = (codename) => {
  /* Get the text field */
  var copyText = document.getElementById("finalcodename");


  let codenames = String(copyText.innerText);

  let url = "https://youareel.heroku.com/" + codenames;
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
