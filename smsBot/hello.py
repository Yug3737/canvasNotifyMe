from pushbullet import Pushbullet

Yug_API_KEY = "o.pRKGXgfyRf6v69A4Vwl0WkdQrkW8THQP"
file = "hello.txt"

with open(file,mode="r") as f:
  text = f.read()

pb = Pushbullet(Yug_API_KEY)
push = pb.push_note("Please remember",text)