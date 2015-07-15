class Tweet < ActiveRecord::Base
	
	require 'date'
	self.primary_key="id"
	TIME_OF_DAY=['morning', 'afternoon', 'evening']
	GENDERS = ['male', 'female']
	TYPES = ['visitors','locals']
	MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']

	scope :morn, ->{ where("EXTRACT(HOUR from created_at) < ?", 12)}
	scope :noon, ->{ where("EXTRACT(HOUR from created_at) BETWEEN ? AND ?", 12, 18)}
	scope :night, ->{ where("EXTRACT(HOUR from created_at) > ?", 18)}
	scope :in_timeline?, ->(days){where("created_at >= ?", Date.today-days)}
	scope :by_user, ->(user_id){where("twitter_user->'id' = ?", user_id)}

	def is_local?(days)
		tweets_by_user = Tweet.by_user(self.twitter_user['id'])
		 	tweets_by_user.each do |tweet|
		 		if tweet.id!=self.id 
		 			if (Date.parse(tweet.created_at.to_s)-Date.parse(self.created_at.to_s)).abs.to_i >= days 
		 				return true 
					end 
		 		end 
		 	end 
		 return false 
	end 

	def self.get_tweet_statistics(days)
		timeline = Hash.new 
		tweets_within_timeline = Tweet.in_timeline?(days)
		tweets_within_timeline.each do |tweet|
			month = Date.parse(tweet.created_at.to_s).mon
			if timeline[month]==nil 
				timeline[month]=0 
			end 
			timeline[month]+=1
		end 
		return timeline
	end 

	def self.get_genders_by_name(time_of_day)
		array = self.get_names(time_of_day)
		get_gender(array)
	end 

	def self.get_max_index(*args)
		length = args[0].length 
		total_array = Array.new(length-1, 0)
		#ignoring last column (unknown gender)
		 for i in 0..(length-2)
		 	for num in 0..(args.length-1)
		 		total_array[i]+=args[num][i]
		 	end
		 end 
		 return total_array.index(total_array.max)
	end 

	def self.get_names(time_of_day)
		if time_of_day=="morn"
			@locations = Tweet.morn
		elsif time_of_day=="noon"
			@locations = Tweet.noon 
		else time_of_day == "night"
			@location == Tweet.night
		end 
		names_array = Array.new 
		@locations.each do |location| 
			name=location.twitter_user['name']  
		    start_index = (name =~ /\w/) 
			end_index = (name =~ /\s/ || name =~ /[^\w-]/)
			if end_index!=nil && start_index!=nil && end_index-start_index>2
				names_array << name[0...(end_index-1)].upcase 
			else 
				name = name.gsub(/[^A-Za-z-]/, '') 
				if name.length>2 
					names_array << name.upcase 
				end 
			end  
		end 
		return names_array
	end 

	def self.get_gender(names)
		#[males, females, unaccounted]
		gender_array = [0,0,0]
		names.each do |name|
			if Name.find_name(name).female.length>=1 
				gender_array[1]+=1 
			elsif Name.find_name(name).male.length>=1
				gender_array[0]+=1  
			else 
				gender_array[2]+=1 
			end 
		end 
		return gender_array
	end 

	def self.find_max_tweets
		lengths= [Tweet.morn.length,Tweet.noon.length,Tweet.night.length]
		max_index=lengths.index(lengths.max)
		return TIME_OF_DAY[max_index]
	end 


	def self.search(search,timeday="none",gender="none")
		if timeday && timeday.upcase=="AM"
			Tweet.where('text ~* ?',"[\s_.!$#\"'<>@]*#{search}[\s_.!$#\"'<>@]*").morn 
		elsif timeday && timeday.upcase=="PM" 
			Tweet.where('text ~* ?',"[\s_.!$#\"'<>@]*#{search}[\s_.!$#\"'<>@]*").noon
		else
			Tweet.where('text ~* ?',"[\s_.!$#\"'<>@]*#{search}[\s_.!$#\"'<>@]*")
		end 
	end 

	def self.loose_search(search)
		if search 
			Tweet.where('text LIKE ?',"#{search}") 
		else 
			Tweet.all
		end 
	end 

end
