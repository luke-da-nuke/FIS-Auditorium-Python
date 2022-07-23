var allids = ["AllRng", "GallaryRng", "PublicFRng", "PublicBRng", "StageRng"] //All HTML group id's
var allBtnOnID = ["AllRngBtnOn", "GallaryRngBtnOn", "PublicFRngBtnOn", "PublicBRngBtnOn", "StageRngBtnOn"]
var allBtnOffID = ["AllRngBtnOff", "GallaryRngBtnOff", "PublicFRngBtnOff", "PublicBRngBtnOff", "StageRngBtnOff"]
  function testt(){
    console.log("test test");
  }
  function RangeFunc(id, btnID, OppositebtnID, state) { //func for changing slider value when pressing btn| state = on/off
    var slider = document.getElementById(id);
    if (state == "on"){
      document.getElementById(btnID).style.boxShadow = "4px 4px 0 #F4CD8A"; //makes it easier to see which button is on
      document.getElementById(OppositebtnID).style.boxShadow = "none";
      slider.value = "255"
    }
    if (state == "off"){
      document.getElementById(btnID).style.boxShadow = "4px 4px 0 #F4CD8A";
      document.getElementById(OppositebtnID).style.boxShadow = "none";
      slider.value = "0"
    }
  }

  function RangeFuncAll(state) { //func for changing all slider values when using 'all' btns
    if (state == "on")
      var i = 0
      while (allids.length > i){
        document.getElementById(allBtnOnID[i]).style.boxShadow = "4px 4px 0 #F4CD8A"; //sorts through list of button IDs making them light up
        document.getElementById(allBtnOffID[i]).style.boxShadow = "none";
        document.getElementById(allids[i]).value = 255; //sorts thru list with all id's
        i++;
      }
    if (state == "off")
      var i = 0
      while (allids.length > i){
        document.getElementById(allBtnOffID[i]).style.boxShadow = "4px 4px 0 #F4CD8A";
        document.getElementById(allBtnOnID[i]).style.boxShadow = "none";
        document.getElementById(allids[i]).value = 0;
        i++;
      }
  }

  function RangesyncAll(){ //Syncs all sliders to 'all' slider
    AllSlider = document.getElementById("AllRng")
    i = 0
    http.open('POST', 'http://127.0.0.1:5000/slider_update')
    http.send(AllSlider.value)
    console.log(AllSlider.value)
    while (allids.length > i){
      x = document.getElementById(allids[i])
      x.value = AllSlider.value
      i++
    }
  }