class Climate < ActiveRecord::Base
		scope :for_date, -> (date){ where(EST: date) }
		scope :for_month, -> (date){ where(EST: date) }

		def self.meantemp(date)
			data = self.for_date(date)
			data.each do |weatherdata|
				temp=weatherdata.Mean_TemperatureF
				return temp 
			end 
		end 

		def self.averagetemp(date)
			begin_date = date.at_beginning_of_month
			end_date = date.end_of_month 
			sum=0
			begin_date.upto(end_date) do |date| 
				data = self.for_date(date)
				data.each do |weatherdata|
					sum+=weatherdata.Mean_TemperatureF
				end 
			end
			return sum/(end_date.day-begin_date.day+1)
		end 
end
