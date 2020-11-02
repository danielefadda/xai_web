// General.
var pkg = require('./package.json');
var project = pkg.name;
var project = project.replace(/_/g, " ");
var slug = pkg.slug;

// Translation.
var packageName = project;
var bugReport = pkg.author_uri;
var lastTranslator = pkg.author;
var team = pkg.author_shop;

// pug.
var pugSRC = './src/*.pug';

// Styles.
var styleSRC = './src/scss/style.scss';
var styleDestination = './_demo/assets/css/';
var cssFiles = './**/*.css';
var scssDistFolder = './docs/scss/';

// Bootstrap.
var bootstrapStyles = './src/scss/bootstrap.scss';
var gutenbergStylesDestination = './_demo/assets/css/';

// CSS Vendor related.
var cssVendorSRC = [
	'node_modules/magnific-popup/dist/magnific-popup.css',
	'node_modules/flickity/dist/flickity.min.css'
];
var cssVendorDestination = './_demo/assets/css/'; // Path to place the compiled JS vendors file.
var cssVendorFile = 'vendors'; // Compiled JS vendors file name.

// JS Vendor related.
var jsVendorSRC = [
	'node_modules/jquery/dist/jquery.min.js',
	'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js',
	'node_modules/flickity/dist/flickity.pkgd.min.js',
	'node_modules/magnific-popup/dist/jquery.magnific-popup.min.js',
	'node_modules/jquery-countto/jquery.countTo.js',
	'node_modules/jquery-countdown/dist/jquery.countdown.js',
	'node_modules/aos/dist/aos.js',
	'node_modules/lozad/dist/lozad.min.js'
];
var jsVendorDestination = './_demo/assets/js/'; // Path to place the compiled JS vendors file.
var jsVendorFile = 'vendors'; // Compiled JS vendors file name.

// JS Custom related.
var jsCustomSRC = './src/js/*.js'; // Path to JS custom scripts folder.
var jsCustomDestination = './_demo/assets/js/'; // Path to place the compiled JS custom scripts file.
var jsCustomFile = 'global'; // Compiled JS custom file name.

// PHP related.
var PHPSRC = [
	'./src/php/**.php'
];
var PHPDestination = './_demo/assets/php/'; // Path to place the compiled JS vendors file.

// Images related.
var imagesSRC = './src/images/**/*.{png,jpg,gif,svg,ico}'; // Source folder of images which should be optimized.
var imagesDestination = './_demo/assets/images/'; // Destination folder of optimized images. Must be different from the imagesSRC folder.

// BrowserSync.
var styleWatchFiles = ['./src/scss/**/*.scss'];
var jsWatchFiles = ['./src/js/**/*.js'];
var projectPHPWatchFiles = ['./**/*.php', '!docs', '!docs/**', '!docs/**/*.php', '!_demo', '!_demo/**', '!_demo/**/*.php'];
var pugWatchFiles = ['./src/*.pug', './src/**/*.pug'];
var htmlWatchFiles = ['./_demo/*.html'];
var imagesWatchFiles = imagesSRC;

// Build.
var distBuildFiles = ['./_demo/**/*'];
var distDestination = './docs/';
var distCleanFiles = ['./docs/'];
var demoCleanFiles = ['./_demo/'];

// Build /slug/ contents within the docs folder
var themeDestination = './docs/';
var themeBuildFiles = './docs/**/*';

// Build _demo contents.
var demoDestination = './_demo/';


// Browsers you care about for autoprefixing. https://github.com/ai/browserslist
const AUTOPREFIXER_BROWSERS = [
	'last 2 version',
	'> 1%',
	'ie >= 9',
	'ie_mob >= 10',
	'ff >= 30',
	'chrome >= 34',
	'safari >= 7',
	'opera >= 23',
	'ios >= 7',
	'android >= 4',
	'bb >= 10'
];

/**
 * Load Plugins.
 */
var gulp = require('gulp');
var pug = require('gulp-pug');
var sass = require('gulp-sass');
var minifycss = require('gulp-uglifycss');
var autoprefixer = require('gulp-autoprefixer');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var del = require('del');
var imagemin = require('gulp-imagemin');
var rename = require('gulp-rename');
var lineec = require('gulp-line-ending-corrector');
var filter = require('gulp-filter');
var sourcemaps = require('gulp-sourcemaps');
var notify = require('gulp-notify');
var browserSync = require('browser-sync').create();
var reload = browserSync.reload;
var sort = require('gulp-sort');
var replace = require('gulp-replace-task');
var zip = require('gulp-zip');
var copy = require('gulp-copy');
var open = require('gulp-open');
var gulpif = require('gulp-if');
var cache = require('gulp-cache');
var gutil = require('gulp-util');
var responsive = require('gulp-responsive');

function clearCache(done) {
	cache.clearAll();
	done();
}

gulp.task(clearCache);

gulp.task('browser-sync', function (done) {
	browserSync.init({
		server: {
			baseDir: "./_demo",
		},
		open: true,
		injectChanges: true,
		notify: false
	});
	done();
});

gulp.task('pug', function (done) {
	return gulp.src(pugSRC)
		.pipe(pug({
			pretty: true
		}))
		.on('error', console.error.bind(console))
		.pipe(replace({
			patterns: [{
					match: 'pkg.name',
					replacement: project
				},
				{
					match: 'pkg.author_shop',
					replacement: pkg.author_shop
				},
				{
					match: 'pkg.author_uri',
					replacement: pkg.author_uri
				},
				{
					match: 'pkg.version',
					replacement: pkg.version
				},
				{
					match: 'pkg.theme_uri',
					replacement: pkg.theme_uri
				},
				{
					match: 'pkg.description',
					replacement: pkg.description
				},
				{
					match: 'pkg.item_title',
					replacement: pkg.item_title
				},
			]
		}))
		.pipe(gulp.dest('./_demo'))
		.pipe(browserSync.stream());
	done();
});


gulp.task('styles', function (done) {
	gulp.src(styleSRC)
		.pipe(sass({
			errLogToConsole: true,
			outputStyle: 'expanded',
			precision: 10
		}))
		.on('error', console.error.bind(console))
		.pipe(autoprefixer(AUTOPREFIXER_BROWSERS))
		.pipe(lineec())
		.pipe(gulp.dest(styleDestination))
		.pipe(filter('**/*.css'))
		.pipe(replace({
			patterns: [{
					match: 'pkg.name',
					replacement: project
				},
				{
					match: 'pkg.author_shop',
					replacement: pkg.author_shop
				},
				{
					match: 'pkg.author_uri',
					replacement: pkg.author_uri
				},
				{
					match: 'pkg.version',
					replacement: pkg.version
				},
				{
					match: 'pkg.theme_uri',
					replacement: pkg.theme_uri
				},
				{
					match: 'pkg.description',
					replacement: pkg.description
				},
				{
					match: 'pkg.item_title',
					replacement: pkg.item_title
				},
			]
		}))
		.pipe(gulp.dest(styleDestination))
		.pipe(browserSync.stream())
	done();
});

gulp.task('bootstrap-styles', function (done) {

	gulp.src(bootstrapStyles, {
			allowEmpty: true
		})

		.pipe(sass({
			errLogToConsole: true,
			outputStyle: 'expanded',
			precision: 10
		}))

		.on('error', console.error.bind(console))

		.pipe(autoprefixer(AUTOPREFIXER_BROWSERS))
		.pipe(rename({
			basename: 'bootstrap',
			suffix: '.min'
		}))
		.pipe(minifycss())
		.pipe(lineec())

		.pipe(gulp.dest(gutenbergStylesDestination))

		.pipe(browserSync.stream())

	done();

});

gulp.task('fontawesome', function (done) {
	return gulp.src([
			'node_modules/@fortawesome/fontawesome-free/css/all.min.css'
		])
		.pipe(rename({
			basename: 'fontawesome-all',
			suffix: '.min'
		}))
		.pipe(gulp.dest('./_demo/assets/css'));
	done();
});

gulp.task('icons', function (done) {
	return gulp.src('node_modules/@fortawesome/fontawesome-free/webfonts/**.*')
		.pipe(gulp.dest('./_demo/assets/webfonts'));
	done();
});

gulp.task('vendor-css', function (done) {
	return gulp.src(cssVendorSRC)
		.pipe(gulp.dest(cssVendorDestination))
	done();
});

gulp.task('scripts', function (done) {

	gulp.src(jsVendorSRC, jsCustomSRC)
		.pipe(lineec())
		.pipe(gulp.dest(jsVendorDestination));

	gulp.src(jsCustomSRC)
		.pipe(lineec())
		.pipe(gulp.dest(jsCustomDestination));

	done();
});

gulp.task('php-files', function (done) {
	gulp.src(PHPSRC)
		.pipe(gulp.dest(PHPDestination));
	done();
});

gulp.task('images', function (done) {
	return gulp.src(imagesSRC)
		.pipe(gulp.dest(imagesDestination))
	done();
});

gulp.task('images-lqip', function (done) {
	return gulp.src('./src/images/**/*.{png,jpg}')
		.pipe(responsive({
			'**/*': {
				quality: 40,
				blur: 70,
				format: 'jpg',
				rename: {
					extname: '-lqip.jpg'
				}
			}
		}))
		.on('error', console.error.bind(console))
		.pipe(gulp.dest(imagesDestination));
	done();
});

gulp.task('clean', function (done) {
	return del(distCleanFiles);
	done();
});

gulp.task('clean_demo', function (done) {
	return del(demoCleanFiles);
	done();
});


gulp.task('copy', function (done) {
	return gulp.src(distBuildFiles)
		.pipe(copy(themeDestination, {
			prefix: 1
		}));
	done();
});

gulp.task('variables', function (done) {
	return gulp.src(themeBuildFiles)
		.pipe(replace({
			patterns: [{
					match: 'pkg.name',
					replacement: project
				},
				{
					match: 'pkg.version',
					replacement: pkg.version
				},
				{
					match: 'pkg.author',
					replacement: pkg.author
				},
				{
					match: 'pkg.author_shop',
					replacement: pkg.author_shop
				},
				{
					match: 'pkg.license',
					replacement: pkg.license
				},
				{
					match: 'pkg.slug',
					replacement: pkg.slug
				},
				{
					match: 'pkg.theme_uri',
					replacement: pkg.theme_uri
				},
				{
					match: 'item_title',
					replacement: pkg.item_title
				},
				{
					match: 'pkg.description',
					replacement: pkg.description
				}
			]
		}))
		.pipe(gulp.dest(themeDestination));
	done();
});

gulp.task('build_notice', function () {
	return gulp.src('./')
		.pipe(notify({
			message: 'Your build of ' + packageName + ' is complete.',
			onLast: false
		}));
});


gulp.task('default', gulp.series('clearCache', 'pug', 'styles', 'bootstrap-styles', 'vendor-css', 'scripts', 'fontawesome', 'icons', 'php-files', 'images', 'images-lqip', 'browser-sync', function (done) {
	gulp.watch(projectPHPWatchFiles, gulp.parallel(reload));
	gulp.watch(pugWatchFiles, gulp.parallel('pug'));
	gulp.watch(styleWatchFiles, gulp.parallel('styles', 'bootstrap-styles'));
	gulp.watch(jsWatchFiles, gulp.parallel('scripts'));
	gulp.watch(imagesWatchFiles, gulp.parallel('images'));

	gulp.watch(htmlWatchFiles).on("change", reload);
	done();
}));

gulp.task('build-process', gulp.series('clearCache', 'clean', 'clean_demo', 'styles', 'bootstrap-styles', 'vendor-css', 'scripts', 'fontawesome', 'icons', 'php-files', 'images', 'images-lqip', 'pug', 'variables', 'copy', function (done) {
	done();
}));

gulp.task('build', gulp.series('build-process', 'build_notice', function (done) {
	done();
}));


