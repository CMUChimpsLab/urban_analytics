# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20150706201224) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"
  enable_extension "hstore"

  create_table "climates", id: false, force: :cascade do |t|
    t.date    "EST"
    t.integer "Max_TemperatureF"
    t.integer "Mean_TemperatureF"
    t.integer "Min_TemperatureF"
    t.integer "Max_Dew_PointF"
    t.integer "MeanDew_PointF"
    t.integer "Min_DewpointF"
    t.integer "Max_Humidity"
    t.integer "Mean_Humidity"
    t.integer "Min_Humidity"
    t.decimal "Max_Sea_Level_PressureIn"
    t.decimal "Mean_Sea_Level_PressureIn"
    t.decimal "Min_Sea_Level_PressureIn"
    t.integer "Max_VisibilityMiles"
    t.integer "Mean_VisibilityMiles"
    t.integer "Min_VisibilityMiles"
    t.integer "Max_Wind_SpeedMPH"
    t.integer "Mean_Wind_SpeedMPH"
    t.integer "Max_Gust_SpeedMPH"
    t.decimal "PrecipitationIn"
    t.integer "CloudCover"
    t.text    "Events"
    t.integer "WindDirDegrees"
  end

  create_table "names", force: :cascade do |t|
    t.string   "name"
    t.string   "gender"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "tweets", id: false, force: :cascade do |t|
    t.text     "contributors"
    t.datetime "created_at",                          null: false
    t.hstore   "entities"
    t.integer  "favourite_count"
    t.text     "filter_level"
    t.integer  "id",                        limit: 8
    t.text     "id_str"
    t.text     "in_reply_to_screen_name"
    t.integer  "in_reply_to_status_id",     limit: 8
    t.text     "in_reply_to_status_id_str"
    t.integer  "in_reply_to_user_id",       limit: 8
    t.text     "in_reply_to_user_id_str"
    t.text     "lang"
    t.hstore   "place"
    t.integer  "retweet_count"
    t.text     "source"
    t.text     "text"
    t.hstore   "twitter_user"
    t.text     "user_screen_name"
    t.text     "coordinates"
  end

end
