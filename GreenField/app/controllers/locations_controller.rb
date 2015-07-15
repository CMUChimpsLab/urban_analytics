class LocationsController < ApplicationController
	def index
		limit=50
		@locations = Tweet.search(params[:keyword], params[:daytime]).paginate(:page => params[:page]).per_page(limit)
		@locations_morning=Tweet.search(params[:keyword], params[:daytime]).morn.paginate(:page => params[:page]).per_page(limit)
		@locations_afternoon=Tweet.search(params[:keyword], params[:daytime]).noon.paginate(:page => params[:page]).per_page(limit)
		@locations_evening=Tweet.search(params[:keyword], params[:daytime]).night.paginate(:page => params[:page]).per_page(limit)

		@morn_gender_array=@locations.get_genders_by_name('morn')
		@noon_gender_array = @locations.get_genders_by_name('noon')
		@evening_gender_array = @locations.get_genders_by_name('night')

	end 

	def for_dates
		redirect_to locations_url
	end 

	def new 
		@keyword=Location.new
	end 

	def show
	end 


	def create
		if !(params[:keyword]).nil?
			redirect_to locations_url[:word]
		  # success
		else
			redirect_to home_url
		  # error handling
		end
	end 
end

# select 
# SELECT * FROM hstore_test WHERE data ? 'key4'


