////////////////////////////
///    CONFIGURE GRID    ///
////////////////////////////

// Configure primary grid with 16 columns.
grid-columns = 16
grid-column-width = 60px
grid-gutter = 32px

// Configure nested grid
//  - assumes space of 8 columns of parent grid.
//  - configures 3 inner columns
//  - configured gutter of 64px for inner columns
ngrid-1-ocolumns = 8
ngrid-1-icolumns = 4
ngrid-1-gutter = 64px


////////////////////////////
///      VARIABLES       ///
////////////////////////////

fcolor_light     = #ffffff
fcolor_dark      = #000000
fcolor_active    = #eb7f13

bcolor_aqua     = darken(#0da0b0 10%)
bcolor_offwhite = #f0f0f0
bcolor_lgrey    = #dddddd
bcolor_dgrey    = #181818

cvig_one = #585b9b
cvig_two = #3b8b87
cvig_three = #39649d
cvig_four = #3e5c7c


/////////////////////////
///      STYLES       ///
/////////////////////////

h1
    font-family: "AsapBold"
    font-size: 64px
    letter-spacing: 4px
    text-transform: uppercase

h2
    font-family: "AsapRegular"
    font-size: 28px
    line-height: 32px
    margin-bottom: 16px

h3
    font-family: "AsapRegular"
    font-size: 22px

h4
    font-family: "AsapRegular"
    font-size: 18px

p, label
    font-family: "AsapRegular"
    font-size: 16px

strong
    font-weight: normal
    font-family: "AsapBold"


body
    position: relative
    top: 80px

    > section
        padding: 40px 16px
        line-height: 1.4em

        .main
            (d) col(13)

            (d) .item
                ncol(1 9)
                margin-bottom: 24px

            aside
                width: 100%
                (d) ncol(1 4)

        (d) h2
            ncol(1 3)

header
    nav
        background: #111111
        height: 80px
        position: fixed
        top: 0px
        left: 0px
        z-index: 1000
        width: 100%
        group()

        ul
            width: 100%
            text-align: center

            li
                display: inline-block

#banner
    width: 100%
    height: 440px
    text-align: center
    background: url("/images/banner.jpg") no-repeat scroll left center
    group()

    #bannerbox
        padding: 36px 0
        margin: 124px auto 0
        position: relative
        width: 100%
        background-color: rgba(0,0,0, 0.5)
        group()

    h1
        color: white
        text-shadow: 4px 4px 8px fcolor_dark


    .subtitle
        text-transform: lowercase
        font-size: 18px
        font-family: "AsapRegular"
        letter-spacing: 2px
        text-shadow: 2px 2px 8px fcolor_dark
        margin-top: 6px

        a
            display: block
            (d) display: inline
            outline: none
            text-decoration: none
            color: white
            margin-bottom: 6px

        .divider
            display: none
            (d) display: inline
            color: white

#about
    background: bcolor_aqua
    color: fcolor_light

    p
        margin-bottom: 12px

    aside
        vertical-align: middle
        text-align: center

    a
        vertical-align: middle
        color: fcolor_light
        text-decoration: none
        font-size: 20px
        font-family: "AsapBold"

        &:hover
            .dmicon-printer
                transform: scale(1.1, 1.1)

    .dmicon-printer
        font-size: 32px
        margin-right: 12px
        display: inline-block
        vertical-align: middle
        transition: transform 0.25s
        -webkit-transition: -webkit-transform 0.25s
        transition-timing-function: ease-in-out


#resume
    background: bcolor_offwhite
    color: fcolor_dark

#involvement
    background: white
    color: fcolor_dark

    h3
        margin-bottom: 8px
    p
        margin-bottom: 16px
    img
        display: inline-block
        text-align: center
        width: 100%
        margin-bottom: 40px


#contact
    background: bcolor_dgrey
    color: fcolor_light

    .testimonial-wrapper
        text-align: center

    .testimonial
        display: inline-block
        text-align: center
        margin-top: 48px

    p.quote
        letter-spacing: 1px

    p.name
        margin-top: 6px
        text-align: right
        font-weight: bold

    fieldset
        border: none
        padding: 0

        label
            display: inline-block
            line-height: 48px
            width: 72px
            float: left
            margin-right: 32px
            (d) text-align: right


        input, textarea, select
            display: inline-block
            width: 100%
            (d) width: 320px
            padding: 14px 20px
            margin-bottom: 12px
            color: rgb(238, 238, 238)
            background: rgb(51, 51, 51)
            border: none
            outline: none

            &:focus
                color: fcolor_light
                background-color: bcolor_aqua

        input.forbotsonly
            display: none

        button
            margin: 16px 0 0 0
            (d) margin: 16px 0 0 104px
            padding: 10px 15px
            background: bcolor_aqua
            color: fcolor_light
            outline: none
            border: none
            font-family: "AsapRegular"
            font-size: 16px
            font-weight: bold
            letter-spacing: 4px
            text-transform: uppercase
            transition: background 0.25s, color 0.25s
            transition-timing-function: ease-in-out

            &:hover
                background: fcolor_active
                color: fcolor_dark

            &::-moz-focus-inner
                border: none

(d) .center
    width: gridwidth
    margin: 0 auto
    position: relative
    group()


footer
    background: #030303
    color: #ffffff

    height: 64px
    padding: 8px 0

    .center
        padding-right: 32px
        text-align: right
        line-height: 48px

    a.email
        display: inline-block
        vertical-align: middle
        margin-right: 16px

        font-size: 20px
        color: fcolor_light
        text-decoration: none

    a.dmicon-facebook, a.dmicon-linkedin
        display: inline-block
        vertical-align: middle
        margin-left: 24px

        font-size: 24px
        color: fcolor_light
        text-decoration: none


.dmicon-about, .dmicon-resume, .dmicon-contact, .dmicon-work
    display: inline-block
    font-size: 32px
    text-decoration: none
    color: fcolor_light
    text-shadow: 0 0 10px bcolor_dgrey
    padding: 24px
    transition: text-shadow 0.5s, transform 1s
    transition-timing-function: ease-out
    -webkit-transition: text-shadow 0.5s, -webkit-transform 1s;

    &:hover
        text-shadow: 0 0 14px bcolor_aqua
        transform: scale(1.1, 1.1)
        transition: text-shadow 0.5s, transform 1s
        -webkit-transition: text-shadow 0.5s, -webkit-transform 1s

    &:focus
        outline: none



(m) .dmicon-resume, #resume
    display: none !important


/////////////////////////
///    INFOGRAPHIC    ///
/////////////////////////

#cvig
    width: 808px
    height: 928px
    margin-left: 76px
    position: relative

    div
        position: absolute

    .bg
        #banner
            left: 172px
            top: 23.3px
            width: 466px //464px
            height: 82px //80.5px
            transform-origin: 232px 40.25px // center
            background-image: url('/images/cvig/banner.svg');

            transition: transform 0.25s ease-in-out
            -webkit-transition: -webkit-transform 0.25s ease-in-out

            &:hover
                transform: scale(1.02, 1.02)

        #timeline
            left: 34.4px
            top: 121.6px
            width: 157px //155.9px
            height: 768px //765.7px
            background-image: url('/images/cvig/timeline.png');


        .block
            .label
                opacity: 0
                transform: scale(0, 0)
                -webkit-transform: scale(0, 0)
                transition: opacity 0.50s ease-in-out 0.20s
                -webkit-transition: opacity 0.25s ease-in-out
                z-index: 5

            .box
                cursor: hand
                cursor: pointer
                transform: scale(1, 1)
                transform-origin: 0px 0px
                transition: transform 0.25s ease-in-out
                -webkit-transition: -webkit-transform 0.25s ease-in-out

            &#one
                .box
                    left: 196px
                    top: 537.9px
                    width: 69.0px
                    height: 275.6px
                    background: cvig_one

                .label
                    left: 272px
                    top: 659.7px
                    width: 191px
                    height: 35px
                    background-image: url('/images/cvig/label-one.png');

            &#two
                .box
                    left: 196px
                    top: 346.0px
                    width: 69.0px
                    height: 191.8px
                    background: cvig_two

                .label
                    left: 272px
                    top: 426px
                    width: 259px
                    height: 35px
                    background-image: url('/images/cvig/label-two.png');

            &#three
                color: blue
                .box
                    left: 196px
                    top: 284.3px
                    width: 69.0px
                    height: 61.7px
                    background: cvig_three

                .label
                    left: 272px
                    top: 299.2px
                    width: 127px
                    height: 35px
                    background-image: url('/images/cvig/label-three.png');

            &#four
                .box
                    left: 196px
                    top: 152px
                    width: 69.0px
                    height: 132.3px
                    background: cvig_four

                .label
                    left: 272px
                    top: 202.2px
                    width: 219px
                    height: 35px
                    background-image: url('/images/cvig/label-four.png');

            &:hover
                .box
                    transform: scale(0.8, 1)
                    -webkit-transform: scale(0.8, 1)

                .label
                    opacity: 1
                    transform: scale(1, 1)
                    -webkit-transform: scale(1, 1)

    .job
        opacity: 0
        transition: opacity 0.25s ease-in-out

        .title
            left: 278px //278.5px
            top: 152px
            width: 500px
            height: 58px
            transform-origin: 528px 181px  // center
            color: white

            font-family: "AsapBold"
            font-size: 32px
            text-align: center
            vertical-align: middle
            line-height: 64px //58px

        .bar
            left: 293px
            top: 224px
            width: 26px
            height: 590px
            transform: scale(1, 0)
            transform-origin: 13.25px 0px  // top-center
            background: black

        .text
            left: 348px
            top: 242px
            width: 397px
            height: 540px

            font-family: "AsapRegular"
            font-size: 18px

            b
                font-family: "AsapBold"

        &#one
            .title, .bar
                background: cvig_one
        &#two
            .title, .bar
                background: cvig_two
        &#three
            .title, .bar
                background: cvig_three
            a
                color: darken(cvig_three 40%)
        &#four
            .title, .bar
                background: cvig_four


    //  CLICK TRANSITIONS
    .cvigActive
        z-index: 4
        opacity: 1
        transition: opacity 0.25s ease-in-out 0.25s

        .bar
            transform: scale(1, 1)
            transition: transform 0.25s ease-in-out 0.60s
            -webkit-transition: -webkit-transform 0.25s ease-in-out 0.60s


///////////////////////
///    ICON FONT    ///
///////////////////////

@font-face
    font-family: 'divmain'
    src: url("/fonts/divmain.eot")
    src: url("/fonts/divmain.eot?#iefix") format('embedded-opentype'), url("/fonts/divmain.woff") format('woff'), url("/fonts/divmain.ttf") format('truetype'), url("/fonts/divmain.svg#divmain") format('svg')
    font-weight: normal
    font-style: normal

.dmicon-about, .dmicon-resume, .dmicon-contact, .dmicon-work, .dmicon-printer, .dmicon-adobe, .dmicon-facebook, .dmicon-linkedin
    font-family: 'divmain'
    speak: none
    font-style: normal
    font-weight: normal
    font-variant: normal
    text-transform: none
    line-height: 1
    -webkit-font-smoothing: antialiased

.dmicon-about:before
    content: "\e000"

.dmicon-resume:before
    content: "\e001"

.dmicon-work:before
    content: "\e003"

.dmicon-contact:before
    content: "\e002"

.dmicon-printer:before
    content: "\e004"

.dmicon-adobe:before
    content: "\e005"

.dmicon-facebook:before
    content: "\e006"

.dmicon-linkedin:before
    content: "\e007"


////////////////////////
///   DISPLAY FONT   ///
////////////////////////

@font-face
    font-family: 'AsapRegular'
    src: url('/fonts/Asap-Regular-webfont.woff') format('woff'), url('/fonts/Asap-Regular-webfont.svg#AsapRegular') format('svg')
    font-weight: normal
    font-style: normal

@font-face
    font-family: 'AsapBold'
    src: url('/fonts/Asap-Bold-webfont.woff') format('woff'), url('/fonts/Asap-Bold-webfont.svg#AsapBold') format('svg')
    font-weight: normal
    font-style: normal


////////////////////
///    OUTPUT    ///
////////////////////

(root)
(root.d) @media screen and (min-width: 970px)
(root.m) @media screen and (max-width: 970px)
