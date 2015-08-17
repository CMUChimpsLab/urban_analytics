class EnableHstore < ActiveRecord::Migration
	def change
    reversible do |op|
      op.up { enable_extension 'hstore' }
    end
  end
end
