/*************************************************************************
TripBuddy.sg (c) 2016. All rights reserved.
*************************************************************************/

function configureDropDownLists(university, school) {
    var NTU = ['Nanyang Business School', 'School of Chemical and Biomedical Engineering', 'School of Civil and Environmental Engineering', 'School of Computer Engineering', 'School of Electrical and Electronic Engineering', 'School of Materials Science and Engineering', 'School of Mechanical and Aerospace Engineering', 'School of Art, Design and Media', 'School of Humanities and Social Sciences', 'Wee Kim Wee School of Communication and Information', 'School of Biological Sciences', 'School of Physical and Mathematical Sciences', 'Lee Kong Chian School of Medicine'];
    var NUS = ['Faculty of Arts & Social Sciences', 'NUS Business School', 'School of Computing', 'Faculty of Dentistry', 'School of Design & Environment', 'Faculty of Engineering', 'Yong Loo Lin School of Medicine', 'Faculty of Science', 'Lee Kuan Yew School of Public Policy', 'Faculty of Law'];
    var SMU = ['School of Accountancy', 'Lee Kong Chian School of Business', 'School of Economics', 'School of Information Systems', 'School of Law', 'School of Social Sciences'];

    switch (university.value) {
    case 'Nanyang Technological University':
        school.options.length = 0;
        createOption(school, "", "");
        for (i = 0; i < NTU.length; i++) {
            createOption(school, NTU[i], NTU[i]);
        }
        break;
    case 'National University of Singapore':
        school.options.length = 0;
        createOption(school, "", "");
        for (i = 0; i < NUS.length; i++) {
            createOption(school, NUS[i], NUS[i]);
        }
        break;
    case 'Singapore Management University':
        school.options.length = 0;
        createOption(school, "", "");
        for (i = 0; i < SMU.length; i++) {
            createOption(school, SMU[i], SMU[i]);
        }
        break;
    default:
        school.options.length = 0;
        createOption(school, "", "");
        break;
    }
}

function createOption(ddl, text, value) {
    var opt = document.createElement('option');
    opt.value = value;
    opt.text = text;
    ddl.options.add(opt);
}