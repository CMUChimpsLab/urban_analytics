class CreateClimates < ActiveRecord::Migration
  def change
    create_table :climates do |t|
      t.date :EST
      t.integer :Max_TemperatureF
      t.integer :Mean_TemperatureF
      t.integer :Min_TemperatureF
      t.integer :Max_Dew_PointF
      t.integer :MeanDew_PointF
      t.integer :Min_DewpointF
      t.integer :Max_Humidity
      t.integer :Mean_Humidity
      t.integer :Min_Humidity
      t.decimal :Max_Sea_Level_PressureIn
      t.decimal :Mean_Sea_Level_PressureIn
      t.decimal :Min_Sea_Level_PressureIn
      t.integer :Max_VisibilityMiles
      t.integer :Mean_VisibilityMiles
      t.integer :Min_VisibilityMiles
      t.integer :Max_Wind_SpeedMPH
      t.integer :Mean_Wind_SpeedMPH
      t.integer :Max_Gust_SpeedMPH
      t.decimal :PrecipitationIn
      t.integer :CloudCover
      t.text :Events
      t.integer :WindDirDegrees

      t.timestamps null: false
    end
  end
end
