// this var is used to set the amount of time the user has
          // the foramt is in seconds
          var prepTime = 240
          var speakingTime = 120
          
          // I have no idea how this work it but it stops the startPrepTimer callback for 5 seconds
          function resolveAfter5Seconds(x) {
              return new Promise((resolve) => {
                setTimeout(() => {
                  resolve(x);
                }, 5000);
              });
            }
            
          
          function startPrepTimer(_callback){
              var current = 0
              //timer var is setup here because it is needed later to shutoff the setInterval func
              // the setInterval function is used to call the function every second
              // the function is used to increment the current var by 1
              var timer = setInterval(async function(){
                  current++
                  document.getElementById("timerTitle").innerHTML= "Prep Time left:"
                  //used for debugging
                  //console.log(current)
                  var timeLeft = prepTime - current
                  // this is used to convert the time left into minutes and seconds
                  var minutes = Math.floor((timeLeft % ( 60 * 60)) / ( 60));
                  var seconds = Math.floor((timeLeft % 60) );
                  // this is used to display the time left to the user
                  document.getElementById("timer").innerHTML= minutes + "m " + seconds + "s "
                  // this is used to stop the timer and start the speaking timer
                  if(prepTime <= current){
                    document.getElementById("timerTitle").innerHTML= ""
                     document.getElementById("timer").innerHTML= "Prep time is over. Start recording."
                    // this is used to stop the timer so it does not keep running
                    clearInterval(timer)
                    // some stuff that stops the callback for 5 seconds
                    // not sure how it works but it does
                    console.log(await resolveAfter5Seconds("waited 5 seconds"))
                    // this is used to start the speaking timer
                    _callback()
                }
              }, 1000)
                 
          }
          //
          function startTimer(){
              //uses a call back to start the speaking timer
              startPrepTimer(function(){
                  var current = 0
                  var timer = setInterval(function(){
                      current++
                        document.getElementById("timerTitle").innerHTML= "Speaking Time left:"
                      //console.log(current)
                      var timeLeft = speakingTime - current
                      var minutes = Math.floor((timeLeft % ( 60 * 60)) / ( 60));
                      var seconds = Math.floor((timeLeft % 60) );
                      document.getElementById("timer").innerHTML= minutes + "m " + seconds + "s "
                      if(speakingTime <= current){
                            document.getElementById("timerTitle").innerHTML= ""
                          document.getElementById("timer").innerHTML= "Time is up. End recording and upload."
                          clearInterval(timer)
                      }
                  }, 1000)
              })
          }
          
          startTimer()