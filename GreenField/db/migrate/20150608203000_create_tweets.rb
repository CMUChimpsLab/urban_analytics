class CreateTweets < ActiveRecord::Migration
  def change
    create_table :tweets, id: false do |t|
      t.text :contributors
      t.timestamp :created_at
      t.hstore :entities
      t.integer :favourite_count
      t.text :filter_level
      t.bigint :id
      t.text :id_str
      t.text :in_reply_to_screen_name
      t.bigint :in_reply_to_status_id
      t.text :in_reply_to_status_id_str
      t.bigint :in_reply_to_user_id
      t.text :in_reply_to_user_id_str
      t.text :lang
      t.hstore :place
      t.integer :retweet_count
      t.text :source
      t.text :text
      t.hstore :twitter_user
      t.text :user_screen_name
      t.point :coordinates

      t.timestamps null: false
    end
  end
end
