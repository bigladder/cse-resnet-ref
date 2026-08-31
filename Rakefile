# Require Modelkit as a library rather than shelling out to the `modelkit` CLI.
# The CLI's `template-compose` command reads a template path from stdin whenever
# stdin isn't a TTY (e.g. any non-interactive invocation: CI, scripts, `system()`
# subprocesses), which silently discards the template argument and fails with
# "No template was referenced!" -- even though the command line was correct.
# Calling the library directly skips the CLI parser entirely, so it isn't exposed
# to that bug. Run via `modelkit rake` so GEM_HOME/GEM_PATH resolve this require.
if (not defined?(Modelkit))
  begin
    require("modelkit")
  rescue LoadError => exception
    puts exception
    puts "ERROR: This rakefile requires the Modelkit library. Try running with:\n  modelkit rake #{ARGV.join(' ')}"
    exit
  end
end

require("modelkit/config")
require("modelkit/parametrics")

require 'fileutils'
require 'pathname'

CONFIG = Modelkit::Config.new(".modelkit-config")

def compose(c)
  file_base = File.basename(c,".*")
  file_dir = Pathname(c).parent.basename

  output_dir = "output/#{file_dir}/#{file_base}"
  #Create output directory
  unless File.directory?(output_dir)
    FileUtils.mkdir_p(output_dir)
  end

  src = ['base.pxt', 'CSE.exe', c]
  target = "#{output_dir}/in.cse"

  puts "================="
  puts "Running case " + file_base + ":"
  puts "=================\n"

  # Compose with modelkit
  success = nil
  if !(FileUtils.uptodate?(target, src))
    puts "\ncomposing...\n\n"
    begin
      Modelkit::Parametrics.template_compose("base.pxt",
        :annotate => CONFIG["template-compose.annotate"],
        :indent => CONFIG["template-compose.indent"],
        :esc_line => CONFIG["template-compose.esc-line"],
        :files => [c],
        :output => target)
      success = true
    rescue Exception => exception
      puts "#{exception.class.name}: #{exception.message}\n"
      puts "#{exception.backtrace.first}\n" if (not SyntaxError === exception)
      success = false
    end
  else
    puts "  ...input already up-to-date."
    success = true
  end
  return success
end

def sim(c)
  file_base = File.basename(c,".*")
  file_dir = Pathname(c).parent.basename

  output_dir = "output/#{file_dir}/#{file_base}"

  src = ["#{output_dir}/in.cse"]
  target = ["#{output_dir}/in.rep", "#{output_dir}/DETAILED.csv"]

  success = nil
  if !(FileUtils.uptodate?(target[0], src)) or !(FileUtils.uptodate?(target[1], src))
    puts "\nsimulating..."
    Dir.chdir(output_dir){
      success = system(%Q|..\\..\\..\\CSE.exe -b -n in.cse|)
    }
    puts "\n"
  else
    puts "  ...output already up-to-date.\n"
    success = true
  end
  return success
end

# example: 'rake sim[section-7, L100AC]' for just one case
# example: 'rake sim[section-7]' for all cases of a test suite
# example: 'rake sim' for all cases of all test suites
desc "Compose and simulate cases"
task :sim, [:tests, :filter] do |t, args|
  args.with_defaults(:tests=>"*", :filter=>"*")
  tests = Dir["cases/#{args.tests}"] # 'section-7', 'hvac', 'dse'
  for t in tests
    cases = Dir["#{t}/#{args.filter}.pxv"]
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
end

task :default, [:filter] => [:sim]

desc "Clean the output directories"
task :clean_output, [:tests, :filter] do |t, args|
  args.with_defaults(:tests=>"*", :filter=>"*")
  outputs = Dir["output/#{args.tests}"]
  puts "Cleaning output..."
  for o in outputs
    cases = Dir["#{o}/#{args.filter}"]
    for c in cases
      FileUtils.remove_dir(c)
    end
  end
  puts "Cleaning output completed."
end

desc "Clean the results CSV"
task :clean_results, [:tests] do |t, args|
  args.with_defaults(:tests=>'*')
  tests = args.tests # 'section-7', 'hvac', 'dse'
  results = Dir["output/#{tests}/Results.csv"]
  puts "Cleaning results CSV..."
  for csv in results
    FileUtils.rm(csv)
  end
  puts "Cleaning results CSVs completed."
end

desc "Clean all outputs and results CSVs"
task :clean_all => [:clean_output, :clean_results]
