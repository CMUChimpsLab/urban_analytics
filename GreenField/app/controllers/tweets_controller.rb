class TweetsController < ApplicationController
	def index
		@tweets = Tweet.paginate(:page => params[:page]).per_page(10)
	end 

	def show
	end 

	def new
	end 

	def edit
	end 

	def create
	end 

	def update
	end 

	def destroy
	end

end
