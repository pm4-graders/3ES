let newScanId = 1

describe('scanner', () => {
  beforeEach(() => {
    cy.intercept('http://127.0.0.1:8000/api/scan/save').as('apiScanSave')
    cy.viewport('iphone-8')
    cy.visit('/#/scanner')
  })
  it('should display scanner', () => {
    cy.get('[data-test="camera-video"]').should('be.visible')

    cy.get('[data-test="take-photo-button"]').should('be.visible')

    cy.get('[data-test="photo-from-gallery-button"]').should('be.visible')
  })

  it('generate snapshot and expect upload result to fail', () => {
    cy.get('[data-test="take-photo-button"]').click()
    //cy.wait(500)
    cy.get('[data-test="submit-modal"]')
    cy.get('[data-test="snapshot"]').should('be.visible')

    cy.get('[data-test="snapshot"]').should('be.visible')
    cy.get('[data-test="submit-button"]').should('be.visible').click()

    cy.wait('@apiScanSave').then((interception) => {
      assert.isFalse(interception.response.body.success)
    })

    cy.get('[data-test="submit-modal"] [data-test="error-alert"]').should('be.visible')
    cy.get('[data-test="reset-button"]').should('be.visible').click()

    cy.get('[data-test="submit-modal"]').should('not.exist')
  })
  it('input image from gallery and except upload to succeed', () => {
    cy.get('[data-test="photo-from-gallery-input"]').selectFile('cypress/assets/scan1.jpg', {
      force: true
    })
    //cy.wait(500)
    cy.get('[data-test="submit-modal"]')
    cy.get('[data-test="snapshot"]').should('be.visible')

    cy.get('[data-test="snapshot"]').should('be.visible')
    cy.get('[data-test="submit-button"]').should('be.visible').click()

    cy.wait('@apiScanSave').then((interception) => {
      assert.isTrue(interception.response.body.success)
      newScanId = interception.response.body.exam.id
    })

    cy.get('[data-test="submit-modal"] [data-test="error-alert"]').should('not.exist')
    cy.get('[data-test="success-badge"]').should('be.visible')

    cy.get('[data-test="submit-modal"]').should('not.exist')
  })
  it('input image from gallery and except fail because of duplication', () => {
    cy.get('[data-test="photo-from-gallery-input"]').selectFile('cypress/assets/scan1.jpg', {
      force: true
    })
    //cy.wait(500)
    cy.get('[data-test="submit-modal"]')
    cy.get('[data-test="snapshot"]').should('be.visible')

    cy.get('[data-test="snapshot"]').should('be.visible')
    cy.get('[data-test="submit-button"]').should('be.visible').click()

    cy.wait('@apiScanSave').then((interception) => {
      assert.isFalse(interception.response.body.success)
    })

    cy.get('[data-test="submit-modal"] [data-test="error-alert"]').should('be.visible')
    cy.get('[data-test="reset-button"]').should('be.visible').click()

    cy.get('[data-test="submit-modal"]').should('not.exist')
  })
})
describe('check corrections', () => {
  beforeEach(() => {
    cy.visit('/#/corrections')
    cy.get('[data-test="logical-exam-select"]').select('Mathematik 1 2023')
  })
  it('should display new scan', () => {
    cy.get('[data-test="logical-exam-select"]').select('Mathematik 1 2023')
    cy.get('[data-test-id="'+newScanId+'"]').should('be.visible')

  })
  it('should be editable and invalidate', () => {
    cy.get('[data-test-id="'+newScanId+'"]').should('not.have.class', 'invalid')
    cy.get('[data-test-id="'+newScanId+'"] input').first().type('8').trigger('change')
    cy.get('[data-test-id="'+newScanId+'"]').should('have.class', 'invalid')
    cy.get('[data-test-id="'+newScanId+'"] input').first().clear()
    cy.get('[data-test-id="'+newScanId+'"] input').first().type('6').trigger('change')
    cy.get('[data-test-id="'+newScanId+'"]').should('not.have.class', 'invalid')
  })
  it('shows scanned image', () => {
    cy.get('[data-test-id="'+newScanId+'"] [data-test="show-exam-button"]').click()
    cy.get('[data-test="exam-image"]').should('be.visible')
  })
  it('delete scan', () => {
    cy.on('window:confirm', () => {
      return true
    })
    cy.get('[data-test-id="'+newScanId+'"] [data-test="delete-exam-button"]').click()
    cy.get('[data-test-id="'+newScanId+'"]').should('not.exist')
  })
})
