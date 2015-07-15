class CreateNames < ActiveRecord::Migration
  def change
    create_table :names do |t|
      t.string :name
      t.string :gender

      t.timestamps null: false
    end
  end
end
