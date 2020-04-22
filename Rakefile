require 'fileutils'

def compose(c)
  file_base = File.basename(c,".*")

  output_dir = 'output/' + file_base
  #Create output directory
  unless File.directory?(output_dir)
    FileUtils.mkdir_p(output_dir)
  end

  src = ['base.pxt', 'CSE.exe', c]
  target = output_dir + '/in.cse'

  puts "================="
  puts "Running case " + file_base + ":"
  puts "=================\n"

  # Compose with modelkit
  success = nil
  if !(FileUtils.uptodate?(target, src))
    puts "\ncomposing...\n\n"
    success = system(%Q|modelkit template-compose -f "#{c}" -o "#{output_dir + '/in.cse'}"  base.pxt|)
  else
    puts "  ...input already up-to-date."
    success = true
  end
  return success
end

def sim(c)
  file_base = File.basename(c,".*")

  output_dir = 'output/' + file_base

  src = [output_dir + '/in.cse']
  target = [output_dir + '/in.rep', output_dir + '/DETAILED.csv']

  success = nil
  if !(FileUtils.uptodate?(target[0], src)) or !(FileUtils.uptodate?(target[1], src))
    puts "\nsimulating..."
    Dir.chdir(output_dir){
      success = system(%Q|..\\..\\CSE.exe -b -n in.cse|)
    }
    puts "\n"
  else
    puts "  ...output already up-to-date.\n"
    success = true
  end
  return success
end

task :sim, [:filter] do |t, args|
  args.with_defaults(:filter=>'*')
  cases = Dir['cases/' + args.filter + '.*']
  for c in cases
    if !compose(c)
      puts "\nERROR: Composition failed..."
      exit
    end
    if !sim(c)
      puts "\nERROR: Simulation failed..."
      exit
    end
  end
end

task :default, [:filter] => [:sim]

desc "Clean the output directory and results CSVs"
task :clean_output, [:filter] do |t, args|
  args.with_defaults(:filter=>'*')
  outputs = Dir['output/' + args.filter]
  puts "Cleaning output..."
  for o in outputs
    FileUtils.remove_dir(o)
  end
  puts "Cleaning output completed."
end

desc "Clean the results CSV"
task :clean_results do
  puts "Cleaning results CSV..."
  results = Dir['output/Results.csv']
  FileUtils.rm(results)
  puts "Cleaning results CSVs completed."
end

desc "Clean outputs and results CSVs"
task :clean => [:clean_output, :clean_results]
