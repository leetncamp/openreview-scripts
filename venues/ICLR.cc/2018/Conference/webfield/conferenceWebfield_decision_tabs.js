// ------------------------------------
// Advanced venue homepage template
//
// This webfield displays the conference header (#header), the submit button (#invitation),
// and a tabbed interface for viewing various types of notes.
// ------------------------------------

// Constants
var CONFERENCE = 'ICLR.cc/2018/Conference';
var INVITATION = CONFERENCE + '/-/Submission';
var BLIND_INVITATION = CONFERENCE + '/-/Blind_Submission';
var WITHDRAWN_INVITATION = CONFERENCE + '/-/Withdrawn_Submission';

var initialPageLoad = true;

// Main is the entry point to the webfield code and runs everything
function main() {
  Webfield.ui.setup('#group-container', CONFERENCE);  // required

  renderConferenceHeader();

  renderConferenceTabs();

  load().then(renderContent);
}

// Load makes all the API calls needed to get the data to render the page
// It returns a jQuery deferred object: https://api.jquery.com/category/deferred-object/
function load() {
  var notesP = Webfield.api.getSubmissions(BLIND_INVITATION, { pageSize: 1000 });

  var withdrawnNotesP = Webfield.api.getSubmissions(WITHDRAWN_INVITATION, { pageSize: 1000 });

  var decisionNotesP = Webfield.api.getSubmissions('ICLR.cc/2018/Conference/-/Acceptance_Decision', {
    noDetails: true,
    pageSize: 1000
  });

  return $.when(notesP, withdrawnNotesP, decisionNotesP);
}


// Render functions
function renderConferenceHeader() {
  Webfield.ui.venueHeader({
    title: 'ICLR 2018 Conference Track',
    subtitle: '6th International Conference on Learning Representations',
    location: 'Vancouver Convention Center, Vancouver, BC, Canada',
    date: 'April 30 - May 3, 2018',
    website: 'http://www.iclr.cc'
  });

  Webfield.ui.spinner('#notes');
}

function renderConferenceTabs() {
  var sections = [
    {
      heading: 'Oral Papers',
      id: 'accepted-oral-papers',
    },
    {
      heading: 'Poster Papers',
      id: 'accepted-poster-papers',
    },
    {
      heading: 'Invited to submit to Workshop',
      id: 'workshop-papers',
    },
    {
      heading: 'Rejected Papers',
      id: 'rejected-papers',
    },
    {
      heading: 'Withdrawn Papers',
      id: 'withdrawn-papers',
    }
  ];

  Webfield.ui.tabPanel(sections, {
    container: '#notes',
    hidden: true
  });
}

function renderContent(notes, withdrawnNotes, decisionsNotes) {

  var notesDict = {};
  _.forEach(notes, function(n) {
    notesDict[n.id] = n;
  });

  var oralDecisions = [];
  var posterDecisions = [];
  var rejectDecisions = [];
  var workshopDecisions = [];

  _.forEach(decisionsNotes, function(d) {

    if (d.content.decision === 'Accept (Oral)') {
      oralDecisions.push(notesDict[d.forum]);
    } else if (d.content.decision === 'Accept (Poster)') {
      posterDecisions.push(notesDict[d.forum]);
    } else if (d.content.decision === 'Reject') {
      rejectDecisions.push(notesDict[d.forum]);
    } else if (d.content.decision === 'Invite to Workshop Track') {
      workshopDecisions.push(notesDict[d.forum]);
    }
  });

  var paperDisplayOptions = {
    pdfLink: true,
    replyCount: true,
    showContents: true
  };

  Webfield.ui.searchResults(
    oralDecisions,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#accepted-oral-papers'})
  );

  Webfield.ui.searchResults(
    posterDecisions,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#accepted-poster-papers'})
  );

  Webfield.ui.searchResults(
    rejectDecisions,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#rejected-papers'})
  );

  Webfield.ui.searchResults(
    workshopDecisions,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#workshop-papers'})
  );

  Webfield.ui.searchResults(
    withdrawnNotes,
    _.assign({}, paperDisplayOptions, {showTags: false, container: '#withdrawn-papers'})
  );



  $('#notes .spinner-container').remove();
  $('.tabs-container').show();

  // Show first available tab
  if (initialPageLoad) {
    $('.tabs-container ul.nav-tabs li a:visible').eq(0).click();
    initialPageLoad = false;
  }
}

// Go!
main();
