import re
import numpy as np

sport = "sport"

# PATTERNS: our templates and responses

p0 = r"(.+) like (.+)"
r0 = [r"What makes you like {1}?", r"Have you ever played {1}?", r"Do you prefer to watch or play {1}?"]  

p1 = r"(.+) have played (.+) for (.+)"
r1 = [r"How long have you played {1}?", r"Why did you start playing {1}"]

p1_1 = r"(.+) have played (.+)"
r1_1 = [(r"How long have you played that sport?"), (r"Why did you start playing that sport?")]

p1_2 = r"yes i have (.+)"
r1_2 = [r"Why have you {0}?", r"How long have you {0}?", r"What made you {0}?"]

p1_3 = r"yes i have"
r1_3 = [(r"Why have you played that sport?"), (r"How long have you played that sport?"), (r"What made you play that sport?")]

p1_4 = r"i have (.+)"
r1_4 = [r"How long have you {0}?", r"Why did you start {0}?"]

p2 = r"i think (.+)"
r2 = [r"Why do you think {0}?", r"What makes you think {0}?", r"Did someone tell you {0}?"]

p3 = r"i prefer to (.+)"
r3 = [r"Why do you prefer to {0}?", r"When do you {0}?"]

p3_1 = r"i prefer (.+)"
r3_1 = [r"Why do you prefer {0}?", r"What makes you prefer {0}?"]

p4 = r"i can (.+)"
r4 = [r"Why can you {0}?", r"Do you like to {0}?"]

p5 = r"i (.+) at (.+)"
r5 = [r"Why do you {0} at {1}?", r"Do you {0} at {1} with anyone else?"]

p5_1 = r"(.+) likes to (.+) at (.+)"
r5_1 = [r"Why does {0} like to {1} at {2}?", r"Does {0} like to {1} at {2} with anyone else?"]

p6 = r"i (.+) when (.+)"
r6 = [r"Why do you {0} when {1}?", r"When else do you {0}?"]

p6_1 = r"(.+) when (.+)"
r6_1 = [r"Why does {0} when {1}?", r"When else does {0}?"]

p7 = r"i (.+) with (.+)"
r7 = [r"Why do you {0} with {1}?", r"Does {1} like to {0}?"]

p8 = r"it is (.+) to (.+)"
r8 = [r"Why do you think it is {0} to {1}?", r"Did someone convince you that it is {0} to {1}?"]

p9 = r"i (.+) because (.+)"
r9 = [r"Why does {1} cause you to {0}?", r"Is {1} a reason for anything else?"]

p10 = r"i like that (.+) is (.+)"
r10 = [r"Is {0} always {1}?", r"Why do you like that {0} is {1}?"]

p11 = r"i believe (.+)"
r11 = [r"Convince me of {0}.", r"What makes you believe {0}?", r"When did you start to believe {0}?"]

p12 = r"(.+) have to (.+)"
r12 = [r"Why do {0} have to {1}?"]

p12_1 = r"i have to (.+)"
r12_1 = [r"Why do you have to {0}?"]

p12_2 = r"(.+) has to (.+)"
r12_2 = [r"Why does {0} have to {1}?"]

p13 = r"(.+) is (.+)"
r13 = [r"What makes {0} {1}?", r"Is it always the case that {0} is {1}?", r"Why do you believe that {0} is {1}?"]

# We use a dictionary to store and templates and their corresponding responses
patterns = {
p0 : r0, 
p1 : r1, p1_1 : r1_1, p1_2 : r1_2, p1_3 : r1_3, p1_4 : r1_4, 
p2 : r2, 
p3 : r3, p3_1 : r3_1, 
p4 : r4, 
p5 : r5, p5_1 : r5_1, 
p6 : r6, p6_1 : r6_1,
p7 : r7, 
p8 : r8, 
p9 : r9, 
p10 : r10, 
p11 : r11, 
p12 : r12, p12_1 : r12_1, p12_2 : r12_2, 
p13 : r13 }

# We create a list of alternate responses (when no template matches)
alternates = ["What is another sport you like?", "Tell me more.", "I'd like to hear more about that.", "What is (another) sport you have played?", "Can you elaborate?"]
# We create a list of possible ways in which the user could say goodbye
exits = ["goodbye", "good bye", "bye"]

# to start the conversation, we run this function with any value for n
def runConversation(n):
	
	# INTRO
	print("ELIZA: Hello user! To exit the conversation at any time, just say goodbye!")
	name = input("ELIZA: What is your name? \n")
	print("ELIZA: Welcome {}! Remember, our topic is sports ".format(name))
	sport = input("ELIZA: What sport would you like to talk about? \n")
	print("ELIZA: Tell me about {}.".format(sport))

	# The conversatin will run until the user gives a departure word
	while True:
		
		# Getting the user's response
		user = input("Your turn now! \n").lower()
		
		# Checking if we need to end the conversation
		if (user.lower() in exits):
			print("ELIZA: Good Bye! Conversation Over")
			return
		m = 0
		
		# STEP 1: Check for a match (more precise)
		for patt in patterns.keys():
			m = re.match(patt, user)
			# Check for each template if we have found a match, and use it if so
			if m:
				p = patt
				inputs = m.groups()
				formats = ["none", "none", "none"]
				for i in range(0, len(inputs)):
					formats[i] = inputs[i]
				# Generate outputs by keying into dictionary and uniformly select one
				outputs = patterns.get(p)
				select = np.random.random_integers(0, len(outputs) - 1)
				output = outputs[select]
				# Respond and Break
				print("ELIZA: ", output.format(formats[0], formats[1]))
				break
		
		# If no match from STEP 1, start STEP 2: check for a search (less precise)
		if (m == None):
			for patt in patterns.keys():
				m = re.search(patt, user)
				# Check for each template if we have found a search, and use it if so
				if m:
					p = patt
					inputs = m.groups()
					formats = ["none", "none", "none"]
					for i in range(0, len(inputs)):
						formats[i] = inputs[i]
					# Generate outputs by keying into dictionary and uniformly select one
					outputs = patterns.get(p)
					select = np.random.random_integers(0, len(outputs) - 1)
					output = outputs[select]
					# Respond and Break
					print("ELIZA: ", output.format(formats[0], formats[1]))
					break
		
		#If no match or search from STEP 1 and STEP 2, start STEP 3: generate a universal response
		if (m == None):
			select = np.random.random_integers(0, len(alternates) - 1)
			print("ELIZA: ", alternates[select])

# Start the conversation on execution of the program
runConversation(1)
