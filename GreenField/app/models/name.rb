class Name < ActiveRecord::Base
	scope :female, ->{where(gender: 'F')}
	scope :male, ->{where(gender: 'M')}
	scope :find_name, -> (name){where(name: name)}
end
